from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()

llm = ChatOpenRouter(
    model="openrouter/free",
    temperature=0
)

response = llm.invoke("Explain RAG in one sentence.")

print(response.content)