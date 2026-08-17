# 📱 Phone Shop AI - Offline RAG Chatbot

An **offline Retrieval-Augmented Generation (RAG) chatbot** built with Python to help retail employees quickly search and understand internal documentation.

The application combines **semantic search using FAISS**, **vector embeddings using SentenceTransformers**, and a **local Qwen LLM** to answer questions based only on the provided documents.

The system is designed for environments where **privacy, offline operation, low latency, and zero API costs** are important.

---

## 🎥 Demo

### Phone Shop AI in Action

![Phone Shop AI Demo](./Demo%20GIF.gif)

> Ask a question about internal documentation and receive a locally generated answer with relevant source references - without sending data to an external API.

---

## Motivation
* While working a part-time job at a mobile shop, I realised employees found it hard to navigate through the portals. Even though there were manuals available, they were too long and not practical. I thought what if we gave these manuals to a chatbot and asked it questions after all the manuals are the heart and soul of the portal. However, it came with a few issues - documents were confidential and could not be shared externally, the shop did not want to spend money and each query incurs a cost.
* Solution - A local chatbot which executes only on the local system. I said let's take a model (Qwen), give it the documents and execute it using the shop computers resources. This way there is no external cost, the documents are not shared either. Privacy and cost both protected.
* Once it was completed with a UI, I realised the PDFs were too long for execution with the model on the local computer's limited hardware capabilites. So instead of matching the user queries throughout the manuals, we break it down into chunks of text and find the nearest match which saves time and computing power.
* Finally it had to be packaged into a user-friendly UI for which I decided to go forward with Tkinter. 
-------------

## ✨ Features

* 🔍 **Semantic search** using FAISS
* 🤖 **Fully local LLM inference** - no external API or API costs
* 📄 Supports multiple PDF documents
* 🧠 **Retrieval-Augmented Generation (RAG)** architecture
* 💬 Desktop GUI built with Tkinter
* 📚 Displays document sources for answers
* 🔒 Works completely offline
* ⚡ Fast retrieval using vector embeddings
* 🖥️ Can be packaged as a standalone Windows executable
* 🛡️ Keeps potentially sensitive business documentation local

---

## 🧠 How It Works

The application follows a complete RAG pipeline:

```text
                         PDF Documents
                              │
                              ▼
                     Extract Text
                       (PyMuPDF)
                              │
                              ▼
                       Split Text
                       into Chunks
                              │
                              ▼
                     Generate Embeddings
                    (SentenceTransformers)
                              │
                              ▼
                       FAISS Index
                              │
════════════════════════════════════════════════════════════
                         User Question
                              │
                              ▼
                    Question Embedding
                              │
                              ▼
                Retrieve Relevant Chunks
                         (FAISS)
                              │
                              ▼
                    Build Context Prompt
                              │
                              ▼
                  Local Qwen 2.5 LLM
                              │
                              ▼
                    Generated Answer
                              │
                              ▼
                  Answer + Source References
```

### Why this architecture?

Instead of sending the entire document collection to an LLM, the system first finds the most relevant pieces of information and provides only that context to the language model.

This makes the system:

* More efficient
* Easier to update
* Less dependent on model training
* Suitable for smaller local models
* Better suited to private/offline environments

---

## 🛠️ Tech Stack

| Technology               | Purpose                  |
| ------------------------ | ------------------------ |
| **Python**               | Application development  |
| **FAISS**                | Vector similarity search |
| **SentenceTransformers** | Text embeddings          |
| **llama-cpp-python**     | Local LLM inference      |
| **Qwen 2.5 1.5B GGUF**   | Local language model     |
| **PyMuPDF**              | PDF text extraction      |
| **NumPy**                | Numerical operations     |
| **Tkinter**              | Desktop GUI              |

---

## 📂 Project Structure

```text
RAG_Chatbot/
│
├── documents/
│   └── PDF knowledge base
│
├── models/
│   └── embeddings/
│
├── index.faiss
│   └── FAISS vector index
│
├── chunks.pkl
│   └── Retrieved document chunks
│
├── rag.py
│   └── RAG pipeline
│
├── main.py
│   └── Main desktop application
│
├── console.py
│   └── Console interface
│
├── Demo GIF.gif
│   └── README demonstration
│
├── requirements.txt
└── README.md
```

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pranayar/RAG_Chatbot.git
cd RAG_Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Download the Language Model

The repository does **not** include the GGUF model because GitHub's file-size limits prevent large model files from being stored directly in the repository.

Download:

**Qwen2.5-1.5B-Instruct Q4_K_M**

Place the downloaded `.gguf` file inside:

```text
models/
```

The model used by the project is:

```text
qwen2.5-1.5b-instruct-q4_k_m.gguf
```

---

## 📄 Add Your Own Documents

The PDF documents used during development are **not included in this public repository**.

They contain proprietary internal documentation and therefore cannot be publicly shared.

To use the chatbot with your own knowledge base:

```text
documents/
├── document1.pdf
├── document2.pdf
├── document3.pdf
└── ...
```

The system can then process these documents and build a searchable vector index.

This also means the chatbot can be adapted to different use cases simply by replacing the document collection.

For example:

* Retail employee support
* IT documentation
* Internal company policies
* Product manuals
* Customer-service knowledge bases
* Technical documentation

---

## 🔎 Building the Vector Index

The indexing pipeline processes the documents by:

1. Reading the PDF files
2. Extracting their text
3. Splitting the text into smaller chunks
4. Generating embeddings
5. Storing the embeddings in a FAISS index
6. Saving the associated text chunks

The resulting files include:

```text
index.faiss
chunks.pkl
```

These files are then used during question answering.

---

## ▶️ Running the Application

### Desktop Application

```bash
python main.py
```

### Console Version

```bash
python console.py
```

---

## 💬 Example Questions

The chatbot can answer questions based on the documents in its knowledge base.

Example queries include:

```text
How do I upgrade a device?

What is the return policy?

How do I activate a SIM card?

How do I transfer a phone number?

What documents are required for verification?
```

The system retrieves relevant document sections before generating the answer.

---

## 🔐 Why Offline RAG?

Traditional chatbot implementations often send user questions and company documentation to cloud-based APIs.

This project takes a different approach:

```text
Traditional Cloud AI

User Question
      ↓
Internet
      ↓
External API
      ↓
Cloud LLM
      ↓
Response
```

This project:

```text
Offline RAG

User Question
      ↓
Local Embedding Model
      ↓
Local FAISS Search
      ↓
Local Document Context
      ↓
Local Qwen LLM
      ↓
Response
```

### Benefits

* 🔒 **Privacy** - documents remain on the local machine
* 🌐 **No internet required**
* 💰 **No API costs**
* ⚡ **Low-latency retrieval**
* 🔄 **Easy document updates**
* 🧠 **No model retraining required when documents change**
* 📚 **Source-aware answers**

---

## 🧩 Retrieval-Augmented Generation

RAG separates **knowledge retrieval** from **language generation**.

Instead of expecting the LLM to memorize company information, the system retrieves relevant information at query time.

```text
             Knowledge Base
                   │
                   ▼
            Vector Embeddings
                   │
                   ▼
              FAISS Index
                   │
                   │
User Question ────┘
       │
       ▼
Similarity Search
       │
       ▼
Relevant Document Chunks
       │
       ▼
Context + Question
       │
       ▼
    Qwen 2.5
       │
       ▼
Generated Response
```

This allows the knowledge base to be updated without retraining the language model.

---

## 📦 Local Model

The project uses:

**Qwen2.5-1.5B-Instruct**

in **GGUF Q4_K_M** format through `llama-cpp-python`.

The relatively small model size makes the system suitable for machines with limited hardware resources compared with larger cloud or local LLM deployments.

---

## 🖥️ Standalone Windows Application

The project can be packaged as a standalone Windows executable so that the target machine does not need a traditional Python development environment.

This makes the system more practical for deployment in a retail or office environment.

---

## ⚠️ Limitations

* The local language model is relatively small and may produce less sophisticated responses than larger LLMs.
* The GGUF model is not included in the repository.
* Proprietary development documents are not included.
* Performance depends on the available CPU/RAM.
* The system is primarily designed for Windows.
* The quality of answers depends on the quality and completeness of the provided documents.
* Scanned PDFs may require OCR before their content can be effectively retrieved.

---

## 🔮 Future Improvements

* [ ] Modernized UI
* [ ] Dark mode
* [ ] Conversation history
* [ ] Streaming responses
* [ ] Improved citation viewer
* [ ] Multi-language support
* [ ] OCR support for scanned PDFs
* [ ] Document management interface
* [ ] Automatic document re-indexing
* [ ] Improved chunking strategies
* [ ] Hybrid keyword + semantic search
* [ ] Reranking retrieved documents
* [ ] Quantized/optimized local models
* [ ] Improved Windows packaging and installation

---

## 🎯 Project Purpose

This project was built to explore how **local Large Language Models, vector databases, embeddings, and Retrieval-Augmented Generation** can be combined to create a practical AI assistant without relying on cloud APIs.

The primary use case is a retail environment where employees need quick access to internal documentation while keeping that information on-premise.

---

## 👨‍💻 Author

**Pranay Arora**

MSc Computer Science

This project demonstrates practical experience with:

* Retrieval-Augmented Generation (RAG)
* Large Language Models
* Vector databases
* Semantic search
* NLP
* Local AI inference
* Python application development
* Desktop application development

---

## 📄 Disclaimer

This project is intended as a demonstration of an **offline Retrieval-Augmented Generation (RAG) system**.

No proprietary documents, confidential information, or copyrighted internal materials are included in this repository.

The application can be used with any compatible PDF document collection.
