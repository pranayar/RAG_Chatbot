import os
import glob
import pickle
import hashlib
import re
import fitz
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

# ===========================
# Configuration
# ===========================

DOCUMENT_FOLDER = "documents"
INDEX_FILE = "index.faiss"
CHUNK_FILE = "chunks.pkl"
HASH_FILE = "documents.hash"

EMBED_MODEL = "models/embeddings/all-MiniLM-L6-v2"
MODEL_PATH = "models/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"

CHUNK_SIZE = 350
CHUNK_OVERLAP = 75
TOP_K = 5


class RAG:

    def __init__(self):

        print("Loading embedding model...")

        self.embedder = SentenceTransformer(EMBED_MODEL)

        print("Loading LLM...")

        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_threads=os.cpu_count() or 2,
            n_batch=256,
            verbose=False
        )

        self.history = []

        if self.needs_rebuild():
            print("Building document index...")
            self.build_index()
        else:
            print("Loading cached index...")
            self.load_index()

        print("Ready!\n")

    # ======================================================
    # Document Hash
    # ======================================================

    def calculate_hash(self):

        md5 = hashlib.md5()

        pdfs = sorted(glob.glob(f"{DOCUMENT_FOLDER}/*.pdf"))

        for pdf in pdfs:

            md5.update(pdf.encode())

            md5.update(str(os.path.getmtime(pdf)).encode())

            md5.update(str(os.path.getsize(pdf)).encode())

        return md5.hexdigest()

    def needs_rebuild(self):

        if not os.path.exists(INDEX_FILE):
            return True

        if not os.path.exists(CHUNK_FILE):
            return True

        if not os.path.exists(HASH_FILE):
            return True

        current = self.calculate_hash()

        with open(HASH_FILE, "r") as f:
            old = f.read().strip()

        return current != old

    def load_index(self):

        self.index = faiss.read_index(INDEX_FILE)

        with open(CHUNK_FILE, "rb") as f:
            self.chunks = pickle.load(f)

        # ======================================================
    # Chunking
    # ======================================================

    def chunk_text(self, text):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + CHUNK_SIZE

            chunk = " ".join(words[start:end]).strip()

            if len(chunk) > 40:
                chunks.append(chunk)

            start += CHUNK_SIZE - CHUNK_OVERLAP

        return chunks


    # ======================================================
    # Build Index
    # ======================================================

    def build_index(self):

        self.chunks = []

        pdfs = sorted(glob.glob(f"{DOCUMENT_FOLDER}/*.pdf"))

        if len(pdfs) == 0:
            raise Exception("No PDFs found inside documents folder.")

        print()

        for pdf in pdfs:

            print(f"Reading {os.path.basename(pdf)}")

            doc = fitz.open(pdf)

            for page_number, page in enumerate(doc):

                text = page.get_text("text")

                if not text.strip():
                    continue

                for chunk in self.chunk_text(text):

                    self.chunks.append({

                        "text": chunk,

                        "source": os.path.basename(pdf),

                        "page": page_number + 1

                    })

        print()

        texts = [c["text"] for c in self.chunks]

        print("Creating embeddings...")

        embeddings = self.embedder.encode(

            texts,

            convert_to_numpy=True,

            show_progress_bar=True

        )

        embeddings = embeddings.astype(np.float32)

        self.index = faiss.IndexFlatL2(

            embeddings.shape[1]

        )

        self.index.add(embeddings)

        faiss.write_index(

            self.index,

            INDEX_FILE

        )

        with open(CHUNK_FILE, "wb") as f:

            pickle.dump(self.chunks, f)

        with open(HASH_FILE, "w") as f:

            f.write(self.calculate_hash())

        print("Index saved.\n")


    # ======================================================
    # Retrieval
    # ======================================================

    def retrieve(self, question):

        embedding = self.embedder.encode(

            [question],

            convert_to_numpy=True

        ).astype(np.float32)

        distances, indices = self.index.search(

            embedding,

            TOP_K

        )

        docs = []

        seen = set()

        for idx in indices[0]:

            if idx == -1:
                continue

            doc = self.chunks[idx]

            key = (doc["source"], doc["page"])

            if key in seen:
                continue

            seen.add(key)

            docs.append(doc)

        return docs

        # ======================================================
    # Chat
    # ======================================================

    
    def chat(self, question, callback=None):

        docs = self.retrieve(question)

        context = "\n\n".join(
            d["text"] for d in docs
        )

        system_prompt = """
    You are an expert assistant for employees of a mobile phone store.

    Rules:
    
    1. Answer from the supplied context.
    2. Never invent information unless there is a source.
    3. If the not sure whether its in the manual do mention:
    "I couldn't find that information in the manuals, but my best guess is.."
    4. Give numbered steps whenever possible.
    5. Keep answers to the point.
    6. Quote menu names exactly as written. Do NOT use **bold**, *, #, tables, or code blocks.
    """
    
        user_prompt = f"""
    Context:
    
    {context}
    
    Question:
    
    {question}
    """
    
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
    
        messages.extend(self.history)
    
        messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )
    
        # --------------------------
        # Stream response
        # --------------------------
    
        stream = self.llm.create_chat_completion(
            messages=messages,
            temperature=0.1,
            top_p=0.9,
            max_tokens=400,
            stream=True
        )
    
        answer = ""
    
        for chunk in stream:
        
            choice = chunk["choices"][0]
    
            delta = choice.get("delta", {})
    
            token = delta.get("content")
    
            if token is None:
                continue
            
            answer += token
    
            if callback is not None:
                callback(token)
    
        answer = answer.strip()
    
        # --------------------------
        # Save conversation history
        # --------------------------
    
        self.history.append(
            {
                "role": "user",
                "content": question
            }
        )
    
        self.history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
    
        # Keep only last 3 exchanges
        if len(self.history) > 6:
            self.history = self.history[-6:]
    
        # --------------------------
        # Sources
        # --------------------------
    
        sources = []
    
        seen = set()
    
        for doc in docs:
        
            src = f"{doc['source']} (Page {doc['page']})"
    
            if src not in seen:
                seen.add(src)
                sources.append(src)
        

        answer = re.sub(r"\*\*(.*?)\*\*", r"\1", answer)   # remove bold
        answer = answer.replace("* ", "• ")               # bullets
        answer = answer.replace("###", "")
        answer = answer.replace("##", "")
        answer = answer.replace("#", "")
        
        return answer, sources

    # ======================================================
    # Clear Conversation
    # ======================================================

    def clear_history(self):
        self.history = []