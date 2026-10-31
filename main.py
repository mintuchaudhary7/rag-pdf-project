from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.retriever import retrieve_documents
from src.prompt import create_prompt
from src.generate_answer import generate_answer


# Create FastAPI application
app = FastAPI()


# Allow requests from the frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mintuchaudhary7.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request body structure
class QuestionRequest(BaseModel):
    question: str


# Complete RAG pipeline
def rag_pipeline(question):

    # 1. Retrieve relevant documents
    documents = retrieve_documents(question, k=3)

    # 2. Create prompt using retrieved documents
    prompt = create_prompt(question, documents)

    # 3. Generate answer using LLM
    answer = generate_answer(prompt)

    return answer


# Home route
@app.get("/")
def home():

    return {
        "message": "RAG API is running"
    }


# Question endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = rag_pipeline(request.question)

    return {
        "question": request.question,
        "answer": answer
    }

