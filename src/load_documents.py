from langchain_community.document_loaders import PyPDFLoader

# file_path = "data/CHO_Problem Solving Using C_4.0.pdf"

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents


# for test 

# documents = load_pdf(file_path)


# print("Number of documents:", len(documents))

# print("\nFirst page:")
# print(documents[0].page_content[:1000])

# print("\nMetadata:")
# print(documents[0].metadata)