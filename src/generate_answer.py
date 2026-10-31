from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()


def generate_answer(prompt):

    llm = ChatOpenRouter(
        model="openrouter/free",
        temperature=0
    )

    response = llm.invoke(prompt)

    return response.content