# PDF RAG Assistant

A Retrieval-Augmented Generation (RAG) application that lets users ask questions about a pre-indexed PDF document. The application retrieves relevant document chunks from a Chroma vector database and uses an LLM through OpenRouter to generate a grounded answer.

## Live Demo

- **Frontend:** https://mintuchaudhary7.github.io/rag-pdf-project/
- **Backend API:** https://rag-pdf-rag-api.onrender.com/
- **API documentation (Swagger):** https://rag-pdf-rag-api.onrender.com/docs
- **GitHub repository:** https://github.com/mintuchaudhary7/rag-pdf-project

> The backend is hosted on Render's free service and may take a short time to wake up after being idle.

## Features

- Ask natural-language questions about an indexed PDF.
- Retrieve relevant text chunks using semantic similarity search.
- Generate context-grounded answers using an OpenRouter chat model.
- Use a persistent Chroma vector database.
- Simple responsive frontend built with HTML, CSS, and vanilla JavaScript.
- FastAPI backend with a `/ask` endpoint.
- Hosted frontend and backend.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python, FastAPI, Uvicorn |
| RAG framework | LangChain |
| PDF parsing | PyPDFLoader / pypdf |
| Text splitting | RecursiveCharacterTextSplitter |
| Embeddings | OpenRouter API — `nvidia/nemotron-3-embed-1b:free` |
| LLM | OpenRouter via LangChain OpenRouter integration (`openrouter/free` routing alias) |
| Vector database | ChromaDB |
| Hosting | GitHub Pages (frontend), Render (backend) |

## How It Works

### 1. Document indexing

The PDF is processed before the application is used:

1. Load the PDF with `PyPDFLoader`.
2. Convert its pages into LangChain `Document` objects.
3. Split the text into overlapping chunks.
4. Generate an embedding vector for each chunk through OpenRouter.
5. Store the chunks and vectors in ChromaDB.

Current text-splitting configuration is approximately **1,000 characters per chunk** with **200 characters overlap**.

### 2. Question answering

When a user asks a question:

1. The frontend sends the question to the backend.
2. FastAPI receives it at `POST /ask`.
3. The question is embedded using the configured OpenRouter embedding model.
4. ChromaDB retrieves the top **3** most relevant chunks.
5. The backend builds a prompt using the question and retrieved context.
6. The OpenRouter chat model generates an answer.
7. The API returns the answer and the frontend displays it.

The prompt instructs the model to answer using the supplied document context and to respond with **“I don't know based on the provided document.”** when the answer is not supported by that context.

## Repository Structure

```text
rag-pdf-project/
├── data/
│   └── CHO_Problem Solving Using C_4.0.pdf
├── chroma_db/
│   └── ...                 # Persisted Chroma vector-store files
├── src/
│   ├── create_embeddings.py
│   ├── ingest.py            # PDF loading, splitting, and indexing
│   ├── retrieve.py          # Similarity retrieval
│   └── ...                  # Prompt / generation helpers
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── main.py                  # FastAPI application and /ask endpoint
├── requirements.txt
├── .env                     # Local secrets; do not commit
├── .env.example             # Example environment variable names
├── .gitignore
├── .python-version           # Render Python version pin
└── README.md
```

> File names inside `src/` may differ slightly depending on the final local version. The main application entry point is `main.py`, and the deployed static site is served from `frontend/`.

## Prerequisites

- Python **3.12** recommended (the deployed environment uses Python 3.12.8).
- Git.
- An OpenRouter API key.
- A PDF document to index.
- Optional: VS Code.

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/mintuchaudhary7/rag-pdf-project.git
cd rag-pdf-project
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Never commit `.env` or expose your API key in frontend JavaScript. Keep the key on the backend only.

### 5. Add or select a PDF

Place the PDF in the `data/` directory. Update the configured PDF path in the ingestion code if you use a different filename.

### 6. Build the vector database

Run the repository's ingestion script from the project root. For example, if the entry point is `src/ingest.py`:

```bash
python -m src.ingest
```

This loads the PDF, splits it, generates embeddings, and persists them in `chroma_db/`.

If your local version uses a different ingestion script name, run that script instead. Do not skip indexing when using a new PDF.

### 7. Start the backend

```bash
uvicorn main:app --reload
```

The API should be available at:

- http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs

### 8. Open the frontend

Open `frontend/index.html` in a browser, or use the VS Code Live Server extension.

For local development, make sure `frontend/script.js` points to the local API:

```javascript
const API_URL = "http://127.0.0.1:8000/ask";
```

The deployed frontend must point to the Render API URL instead.

## How to Use the Application

1. Open the [live demo](https://mintuchaudhary7.github.io/rag-pdf-project/).
2. Wait for the backend to respond if it has been idle.
3. Enter a question about the indexed PDF.
4. Submit the question.
5. Read the generated answer.

Try questions that ask about the document's subject, course details, credits, or other facts present in the indexed PDF. Questions unrelated to the indexed document may return the configured fallback response.

## API Reference

### `GET /`

Health/root endpoint.

**Response example:**

```json
{
  "message": "RAG API is running"
}
```

### `POST /ask`

Ask a question about the indexed document.

**Request:**

```json
{
  "question": "What is this document about?"
}
```

**Response shape:**

```json
{
  "question": "What is this document about?",
  "answer": "..."
}
```

Use the Swagger UI at `/docs` for interactive API testing.

## Deployment

### A. Deploy the backend on Render

1. Push the project to GitHub.
2. Sign in to [Render](https://render.com/) and create a **Web Service** connected to this repository.
3. Leave **Root Directory** blank if `main.py` and `requirements.txt` are at the repository root.
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add the environment variable:
   - `OPENROUTER_API_KEY` = your OpenRouter API key
6. Ensure the service uses the Python version specified in `.python-version` (currently 3.12.8).
7. Deploy and verify the root URL and `/docs`.
8. Confirm that the persisted `chroma_db/` directory is included in the repository and that the backend loads it using a path relative to the project, not a machine-specific absolute path.

**Backend URL:** `https://rag-pdf-rag-api.onrender.com/`

### B. Deploy the frontend on GitHub Pages

1. In `frontend/script.js`, configure the API URL:

   ```javascript
   const API_URL = "https://rag-pdf-rag-api.onrender.com/ask";
   ```

2. Commit and push the changes.
3. In the GitHub repository, open **Settings → Pages**.
4. Use the GitHub Actions deployment workflow configured for the repository to publish the `frontend/` directory.
5. Wait for the workflow to complete.
6. Open the GitHub Pages URL and test a question.

**Frontend URL:** `https://mintuchaudhary7.github.io/rag-pdf-project/`

### C. CORS

The backend must allow requests from the deployed GitHub Pages origin:

```text
https://mintuchaudhary7.github.io
```

For local development, also allow the local frontend origin you use. Since this app does not use cookie-based authentication, credentials should remain disabled unless the authentication design changes.

## Configuration Notes

- The OpenRouter API key is required by the backend for embeddings and generation.
- The `openrouter/free` model name is a routing alias; the underlying model may vary.
- The embedding model returns vectors of 2048 dimensions in the tested configuration. If you change embedding models, rebuild the Chroma collection so stored vectors and query vectors are compatible.
- The Chroma database must be created with the same embedding model used at query time.
- The current application uses a fixed retrieval count (`k=3`).
- Keep the frontend API URL aligned with the environment where the backend is running.

## Troubleshooting

| Problem | What to check |
|---|---|
| Backend does not start | Activate the correct Python environment and install `requirements.txt`. |
| Missing API key | Check that `OPENROUTER_API_KEY` is set in `.env` locally or Render environment settings. |
| Frontend cannot reach API | Verify the API URL in `frontend/script.js`, backend availability, and CORS origin. |
| Render request is slow initially | The free service may be waking after inactivity; retry after it starts. |
| No relevant answer | Confirm the intended PDF was indexed and the `chroma_db/` directory is present. |
| Changed PDF but answers still refer to old content | Re-run ingestion and replace/rebuild the vector database. |
| Embedding dimension/model error | Use the same embedding model for indexing and querying; rebuild the database after model changes. |
| API dependency/build conflict | Use the pinned dependency versions in `requirements.txt` and the Python version in `.python-version`. |

## Current Limitations

- The PDF is indexed ahead of time; users cannot upload PDFs through the web interface.
- The application uses one configured document/vector store.
- Answers are not accompanied by source-page citations in the UI.
- Retrieval uses a fixed top-k value.
- No chat history, streaming responses, user accounts, or document-level access control.
- The free Render service may have cold starts.
- RAG answers depend on the quality of PDF text extraction, chunking, retrieval, and model output.

## Future Improvements

- Add PDF upload and per-document indexing.
- Show retrieved chunks and PDF page references with each answer.
- Support multiple documents and document selection.
- Add conversation history and streaming responses.
- Add retrieval filters, configurable top-k, reranking, and hybrid search.
- Add evaluation tests for retrieval relevance and answer faithfulness.
- Improve deployment/storage strategy for larger vector databases.

## Security

- Keep `OPENROUTER_API_KEY` in backend environment variables only.
- Do not commit `.env`, credentials, or private documents.
- Review the content of PDFs before indexing or making them publicly accessible.
- If the project is extended to private documents or multiple users, add authentication and document-level authorization before deployment.

## Learning Outcomes

This project demonstrates:

- The end-to-end RAG pipeline.
- PDF ingestion and text chunking.
- Embedding generation through an API.
- Vector storage and semantic retrieval with ChromaDB.
- Context-based prompt construction and LLM generation.
- Building a REST API with FastAPI.
- Connecting a vanilla JavaScript frontend to a Python backend.
- Deploying a full-stack AI application using GitHub Pages and Render.

## License

Add a license file if you intend to distribute or reuse this project publicly. Until a license is added, assume the repository's code is not granted an explicit open-source license.
