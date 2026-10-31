import os

from dotenv import load_dotenv
from openrouter import OpenRouter
from langchain_core.embeddings import Embeddings


load_dotenv()


class OpenRouterEmbeddings(Embeddings):

    def __init__(self):

        self.client = OpenRouter(
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        self.model = "nvidia/nemotron-3-embed-1b:free"

    def embed_query(self, text):

        response = self.client.embeddings.generate(
            model=self.model,
            input=text,
            encoding_format="float"
        )

        return response.data[0].embedding

    def embed_documents(self, texts):

        embeddings = []

        for text in texts:

            embedding = self.embed_query(text)

            embeddings.append(embedding)

        return embeddings


def get_embedding_model():

    return OpenRouterEmbeddings()