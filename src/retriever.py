from pathlib import Path
from langchain_chroma import Chroma

from src.create_embeddings import get_embedding_model


# CHROMA_PATH = r"D:\RAG\rag-pdf-project\chroma_db"

CHROMA_PATH = str(Path(__file__).resolve().parent.parent / "chroma_db")

def get_vector_store():

    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vector_store


def retrieve_documents(question, k=3):

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=k
    )

    return documents