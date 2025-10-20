from fastapi import APIRouter, HTTPException
from app.schemas.models import QueryRequest, QueryResponse, SourceDocument
from app.utils.graph import rag_graph
from app.services.retriever_service import retriever

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        # Invoke RAG graph
        result = rag_graph.invoke({"question": request.question})

        # Extract docs safely
        docs = result.get("docs") or []  # ← defaults to empty list if None

        sources = []
        for doc in docs:
            sources.append(SourceDocument(
                content=getattr(doc, "page_content", str(doc)),
                doc_id=getattr(doc.metadata, "doc_id", "unknown") if hasattr(doc, "metadata") else "unknown",
                chunk_index=getattr(doc.metadata, "chunk_index", 0) if hasattr(doc, "metadata") else 0
            ))

        return QueryResponse(
            answer=result.get("answer", ""),
            sources=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")



