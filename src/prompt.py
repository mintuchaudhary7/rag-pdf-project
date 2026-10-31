def create_prompt(question, documents):

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a helpful assistant.

Answer the user's question using only the information provided in the context below.

If the answer cannot be found in the context, say:
"I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt