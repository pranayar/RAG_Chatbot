# 📱 Phone Shop AI - Offline RAG Chatbot

An offline Retrieval-Augmented Generation (RAG) chatbot built with Python to help retail employees quickly search and understand internal documentation.

The application uses semantic search (FAISS) and a local Large Language Model (LLM) to answer questions based only on the provided documents, making it ideal for environments where internet access, privacy, or low latency are important.

---

## Features

- 🔍 Semantic search using FAISS
- 🤖 Fully local LLM inference (no API/Costing required)
- 📄 Supports multiple PDF documents
- 💬 Desktop GUI built with Tkinter
- 📚 Displays document sources for every answer
- 🔒 Works completely offline
- ⚡ Fast retrieval using vector embeddings
- 🖥️ Packaged as a standalone Windows executable

---

## How It Works

```
                PDF Documents
                      │
                      ▼
          Extract Text (PyMuPDF)
                      │
                      ▼
              Split into Chunks
                      │
                      ▼
              Generate Embeddings
           (SentenceTransformers)
                      │
                      ▼
          Store in FAISS Index
──────────────────────────────────────
              User Question
                      │
                      ▼
      Convert Question to Embedding
                      │
                      ▼
     Retrieve Most Relevant Chunks
                      │
                      ▼
      Build Prompt with Context
                      │
                      ▼
      Local Qwen Language Model
                      │
                      ▼
         Answer + Source References
```

---

## Tech Stack

- Python
- Tkinter
- FAISS
- SentenceTransformers
- llama-cpp-python
- PyMuPDF
- NumPy
- Qwen 2.5 1.5B GGUF

---

## Project Structure

```
PhoneShopAI/
│
├── documents/          # PDF knowledge base
├── models/
│   └── embeddings/
├── index.faiss
├── chunks.pkl
├── rag.py
├── main.py
└── console.py
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the language model

The repository does **not** include the GGUF model because GitHub's file size limits prevent uploading large model files.

Download the following model manually:

**Qwen2.5-1.5B-Instruct Q4_K_M**

https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/blob/main/qwen2.5-1.5b-instruct-q4_k_m.gguf

Place the downloaded file inside:

```
models/
```

---

## PDF Documents

The PDF documents used during development are **not included** in this repository.

They contain proprietary internal documentation and therefore cannot be publicly shared.

To use the chatbot, add your own PDF documents into the `documents/` folder and rebuild the vector index.

---

## Building the Vector Index

Run the indexing script (or launch the application if automatic indexing is enabled).

The application will:

- Read all PDFs
- Extract text
- Split into chunks
- Generate embeddings
- Build the FAISS index

---

## Running

```bash
python main.py
```

or

```bash
python console.py
```

---

## Example Questions

- How do I upgrade a device?
- What is the return policy?
- How do I activate a SIM card?
- How do I transfer a phone number?
- What documents are required for verification?

---

## Why RAG?

Instead of training a model on company data, this application retrieves only the most relevant document sections and provides them as context to the language model.

Benefits include:

- Easy document updates
- No model retraining
- Lower hardware requirements
- Source citations for every response
- Reduced hallucinations

---

## Limitations

- Requires local model download (not included in repository)
- Repository does not include proprietary PDF documents
- Designed for Windows (tested with Python 3.11)

---

## Future Improvements

- Modern UI
- Dark mode
- Conversation history
- Streaming responses
- Better citation viewer
- Multi-language support
- OCR support for scanned PDFs
- Document management interface

---

## Disclaimer

This project is intended as a demonstration of an offline Retrieval-Augmented Generation (RAG) system.

No proprietary documents, confidential information, or copyrighted internal materials are included in this repository. The application can be used with any compatible PDF document collection.
