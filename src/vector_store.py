from pathlib import Path

from langchain_chroma import Chroma

from src.create_embeddings import get_embedding_model


# CHROMA_PATH = r"D:\RAG\rag-pdf-project\chroma_db"

CHROMA_PATH = str(Path(__file__).resolve().parent.parent / "chroma_db")


def create_vector_store(chunks):

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    return vector_store