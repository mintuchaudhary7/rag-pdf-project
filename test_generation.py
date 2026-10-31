from src.retriever import retrieve_documents
from src.prompt import create_prompt
from src.generate_answer import generate_answer


question = "What is this document about?"


documents = retrieve_documents(question, k=3)


prompt = create_prompt(question, documents)


answer = generate_answer(prompt)


print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(answer)