from src.create_embeddings import get_embedding_model


embeddings = get_embedding_model()

# print(embeddings , "fvf");

text = "RAG combines retrieval with language model generation."

vector = embeddings.embed_query(text)

print("Vector type:", type(vector))
print("Vector length:", len(vector))
print("First 10 values:", vector[:10])