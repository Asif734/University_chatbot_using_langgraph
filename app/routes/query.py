from fastapi import APIRouter, HTTPException
from app.schemas.models import QueryRequest, QueryResponse, SourceDocument
from app.utils.graph import rag_graph
from app.services.retriever_service import retriever
from app.services.memory_service import MemoryService
# from app.services.redis_service import RedisCacheService



router = APIRouter()
memory_service= MemoryService()
# redis_service= RedisCacheService()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        # Invoke RAG graph
        # cached_answer= redis_service.get_answer(request.question)
        # if cached_answer:
        #     memory_service.add_interaction(
        #     user_id= request.user_id,
        #     question= request.question,
        #     answer= cached_answer
        # )
        #     return QueryResponse(answer= cached_answer, sources= [])


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

        answer= result.get("answer", "")
        memory_service.add_interaction(
            user_id= request.user_id,
            question= request.question,
            answer= answer
        )

        return QueryResponse(
            answer=answer,
            sources=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")



