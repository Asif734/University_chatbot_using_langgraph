import os
from pinecone import Pinecone

class Settings:
    PINECONE_API_KEY = os.getenv(
        "PINECONE_API_KEY",
        "pcsk_5MgxE2_SvtRBE7ARYHwcVd5S5ucZEucguxrL86BCdEovgadhSFoHqDE3CmKVP5nVNRW4cm"
    )
    INDEX_NAME = "multilingual-text"
    LLM_MODEL = "llama3.2:3b"
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ✅ Set it in the environment before LangChain loads Pinecone
os.environ["PINECONE_API_KEY"] = Settings.PINECONE_API_KEY

settings = Settings()
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
