from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path
import os
from config import *

def load_documents_from_folder(folder_path):
    documents = []
    folder = Path(folder_path)
    
    for file_path in folder.rglob('*'):
        if file_path.is_file():
            loader = TextLoader(str(file_path))
            docs = loader.load()
            documents.extend(docs)
    
    return documents

def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

def initialize_vectorstore():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    if os.path.exists(CHROMA_DB_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
    else:

        all_documents = load_documents_from_folder(DOCUMENTS_FOLDER)
        text_splitter = get_text_splitter()
        text_chunks = text_splitter.split_documents(all_documents)
        
        vectorstore = Chroma.from_documents(
            documents=text_chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
    
    return vectorstore


vectorstore = initialize_vectorstore()