import os
from pathlib import Path
from datetime import datetime
import streamlit as st
from langchain_community.llms.ollama import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Constants
PDF_DIR = Path("pdfs")
VECTOR_DB_DIR = Path("vectorstore")
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

PDF_DIR.mkdir(exist_ok=True)
VECTOR_DB_DIR.mkdir(exist_ok=True)

embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
llm = Ollama(model="llama3")


def load_and_split_pdfs(pdf_folder: Path):
    documents = []
    for pdf_file in pdf_folder.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    return chunks


def index_pdfs():
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        return None, "No PDFs found to index.", 0, 0
    chunks = load_and_split_pdfs(PDF_DIR)
    if not chunks:
        return None, "PDFs found but no content extracted.", len(pdf_files), 0
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(str(VECTOR_DB_DIR))
    return vectorstore, "Indexing complete.", len(pdf_files), len(chunks)


def load_vectorstore():
    if not VECTOR_DB_DIR.exists():
        return None
    try:
        return FAISS.load_local(str(VECTOR_DB_DIR), embedding_model, allow_dangerous_deserialization=True)
    except Exception:
        return None


# Session state setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None
if "pdf_count" not in st.session_state:
    st.session_state.pdf_count = 0
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# App UI
st.set_page_config(page_title="Local PDF Chatbot", layout="wide")
st.title("📄 Chat with your PDFs (100% Local)")

# Load or index vectorstore
vectorstore = load_vectorstore()

if not vectorstore:
    vectorstore, msg, pdf_count, chunk_count = index_pdfs()
    if vectorstore:
        st.success(f"{msg} 📄 {pdf_count} PDFs → 🔹 {chunk_count} chunks indexed.")
        st.session_state.last_refresh = datetime.now()
        st.session_state.pdf_count = pdf_count
        st.session_state.chunk_count = chunk_count
    else:
        st.warning(msg)
else:
    st.session_state.pdf_count = len(list(PDF_DIR.glob("*.pdf")))

# Sidebar status
with st.sidebar:
    st.header("📊 Status")
    st.write(f"**PDFs loaded**: {st.session_state.pdf_count}")
    st.write(f"**Chunks**: {st.session_state.chunk_count}")
    st.write(f"**Last refresh**: {st.session_state.last_refresh or 'Never'}")
    if st.button("🔄 Refresh PDFs"):
        with st.spinner("Re-indexing..."):
            vectorstore, msg, pdf_count, chunk_count = index_pdfs()
            if vectorstore:
                st.success(f"{msg}")
                st.session_state.last_refresh = datetime.now()
                st.session_state.pdf_count = pdf_count
                st.session_state.chunk_count = chunk_count
            else:
                st.error(msg)

# Chat UI
if vectorstore:
    prompt_template = """
You are a helpful and aware AI assistant answering questions based on the content of local PDF documents.

You currently have access to {pdf_count} PDF(s), processed into {chunk_count} searchable chunks.

Use the following context to answer the user's question. If the context isn't helpful, use your own general knowledge and clearly say so.

Context:
{context}

Question:
{question}
"""
    prompt = PromptTemplate.from_template(prompt_template).partial(
        pdf_count=st.session_state.pdf_count,
        chunk_count=st.session_state.chunk_count
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question about your PDFs or anything else...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            thinking = st.empty()
            thinking.markdown("🤔 Thinking...")

            try:
                response = qa_chain.run(user_input)
                thinking.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"⚠️ Error: {e}"
                thinking.markdown(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
