import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_pdfs(pdf_folder: str) -> List[Document]:
    """Loads all PDFs from a folder and returns a list of Documents."""
    if not os.path.exists(pdf_folder):
        return []

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    if not pdf_files:
        return []

    documents = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(os.path.join(pdf_folder, pdf_file))
        documents.extend(loader.load())

    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """Splits documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)


def create_vectorstore(documents: List[Document]):
    """Creates and saves a FAISS vectorstore index."""
    if not documents:
        raise ValueError("No documents to index.")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("vectorstore_index")


def load_vectorstore():
    """Loads an existing FAISS vectorstore index."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    index_path = "vectorstore_index"

    if not os.path.exists(os.path.join(index_path, "index.faiss")):
        raise FileNotFoundError("Vectorstore index not found.")

    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
