from src.load_documents import load_pdf
from src.split_documents import split_documents
from src.vector_store import create_vector_store


file_path = "data/CHO_Problem Solving Using C_4.0.pdf"


# 1. Load PDF
documents = load_pdf(file_path)

print("Number of documents:", len(documents))


# 2. Split documents into chunks
chunks = split_documents(documents)

print("Number of chunks:", len(chunks))


# 3. Create vector store
vector_store = create_vector_store(chunks)

print("Vector store created successfully!")