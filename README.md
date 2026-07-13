# chat-with-pdf

A fully local, privacy-centric Retrieval-Augmented Generation (RAG) assistant that allows you to chat with multiple PDF documents simultaneously. Powered by Ollama (LLaMA 3), LangChain, and HuggingFace local embeddings, this application processes all text and vector storage 100% offline.

---

## Features

- **Multi-Document Ingestion**: Parse and query multiple PDF files concurrently.
- **100% Offline Processing**: Zero cloud API dependencies. Your data never leaves your local machine.
- **Dynamic Context Re-indexing**: Live reload system to scan and re-index the local directory when new documents are added.
- **Local Embeddings & Vector Store**: Utilizes local SentenceTransformers for embedding generation and a local vector database for semantic search.
- **Interactive UI**: Clean chat interface built with Streamlit, providing real-time response generation.

---

## Tech Stack

- **Orchestration**: LangChain
- **LLM Engine**: Ollama (LLaMA 3)
- **Vector Database**: Local Vector Store
- **Embeddings Model**: HuggingFace SentenceTransformers
- **User Interface**: Streamlit
- **File Parser**: PyPDF / PDFPlumber

---

## Project Structure

```
chat-with-pdf/
├── app.py               # Core Streamlit application & RAG pipeline
├── requirements.txt     # Python dependency configuration
├── pdfs/                # Local directory for source PDF uploads
├── db/                  # SQLite cache and metadata storage
└── vectorstore/         # Local vector database persistence index
```

---

## Setup & Installation

### Prerequisites
- Python 3.10 or 3.11
- [Ollama](https://ollama.com) installed locally

### Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Pull and Run LLaMA 3**
   Ensure Ollama is running locally and pull the LLaMA 3 model:
   ```bash
   ollama pull llama3
   ```

3. **Incorporate Source Materials**
   Place your target PDF documents in the `pdfs/` folder.

4. **Launch Application**
   ```bash
   streamlit run app.py
   ```
   The application will automatically load in your browser at `http://localhost:8501`.

---

## Future Improvements

- [ ] Add support for metadata filtering to restrict search queries to specific documents.
- [ ] Implement local text-splitting optimizations (e.g. Semantic Chunking).
- [ ] Integrate local cross-encoder re-ranking for improved query retrieval precision.

---

## Author

**Satya**  
GitHub: [programmingxpert](https://github.com/programmingxpert/)
