from langchain_pinecone import Pinecone as LangchainPinecone
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

vectorstore = LangchainPinecone.from_existing_index(
    index_name=settings.INDEX_NAME,
    embedding=embeddings,
    text_key="text"
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
