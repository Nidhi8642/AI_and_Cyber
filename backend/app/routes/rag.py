from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.retriever import search_knowledge_base

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

class RAGSearchRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/search")
def search_rag(request: RAGSearchRequest):
    results = search_knowledge_base(query=request.query, top_k=request.top_k)
    return {
        "query" : request.query,
        "results" : results
    }