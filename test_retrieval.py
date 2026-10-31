from src.retriever import retrieve_documents


question = "What is this document about?"


documents = retrieve_documents(question, k=3)


print("Number of retrieved documents:", len(documents))


for i, document in enumerate(documents):

    print("\n" + "=" * 60)
    print(f"DOCUMENT {i + 1}")
    print("=" * 60)

    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)