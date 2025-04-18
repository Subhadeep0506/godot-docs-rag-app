import sys

sys.path.append("..")

from src.core.query import Query
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.orchastrator import Orchastrator
from src.services.llm_factory import LLMFactory
from src.core.infisical import InfisicalManagedCredentials
from models import QueryRequest, QueryResponse, QueryState

secrets_client = InfisicalManagedCredentials()

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchastrator = Orchastrator()


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        response = orchastrator.generate_response(
            query=request.query,
            category=request.state.category,
            sub_category=request.state.sub_category,
            model_name=request.state.model_name,
            top_k=request.state.top_k,
            session_id=request.session_id,
            memory_service=request.state.memory_service,
            temperature=request.state.temperature,
        )
        return QueryResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/reddit", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        response = orchastrator.generate_reddit_response(
            query=request.query,
            model_name=request.state.model_name,
            temperature=request.state.temperature,
            username=request.state.reddit_username,
            relevance=request.state.relevance,
            top_k=request.state.top_k,
            session_id=request.session_id,
            memory_service=request.state.memory_service,
        )
        return QueryResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
