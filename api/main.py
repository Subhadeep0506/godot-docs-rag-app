import sys

sys.path.append("..")

from src.core.query import Query
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.services.embeddings_factory import EmbeddingsFactory
from src.services.vector_store_factory import VectorStoreFactory
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

embeddings = EmbeddingsFactory().get_embeddings(
    "sentence-transformers", "intfloat/multilingual-e5-large-instruct"
)

vector_store = VectorStoreFactory().get_vectorstore(
    vectorstore_service="astradb",
    embeddings=embeddings,
)


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        llm = LLMFactory().get_chat_model(
            model_name=request.state.model_name,
            temperature=request.state.temperature,
        )
        query_processor = Query(vectorstore=vector_store)

        response = query_processor.generate_response(
            query=request.query,
            category=request.state.category,
            sub_category=request.state.sub_category,
            source=None,
            top_k=request.state.top_k,
            session_id=request.session_id,
            memory_service=request.state.memory_service,
            llm=llm,
        )
        return QueryResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
