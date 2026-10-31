from src.retriever import retrieve_documents
from src.prompt import create_prompt


question = "What is this document about?"


documents = retrieve_documents(question, k=3)


prompt = create_prompt(question, documents)


print(prompt)