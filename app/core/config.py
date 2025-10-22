# import os
# from pinecone import Pinecone

# class Settings:
#     PINECONE_API_KEY = os.getenv(
#         "PINECONE_API_KEY",
#         "pcsk_5MgxE2_SvtRBE7ARYHwcVd5S5ucZEucguxrL86BCdEovgadhSFoHqDE3CmKVP5nVNRW4cm"
#     )
#     INDEX_NAME = "multilingual-text"
#     LLM_MODEL = "gemma3:4b"
#     EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

#     # Gemini model (optional)
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBw_vv1SHpPSjd_14RDbNyLolPNl5kkrIs")
#     GEMINI_MODEL = "gemini-2.5-flash"

# # ✅ Environment setup
# os.environ["PINECONE_API_KEY"] = Settings.PINECONE_API_KEY
# os.environ["GOOGLE_API_KEY"] = Settings.GEMINI_API_KEY

# settings = Settings()
# pc = Pinecone(api_key=settings.PINECONE_API_KEY)





import os
from pinecone import Pinecone

class Settings:
    # Pinecone setup
    PINECONE_API_KEY = os.getenv(
        "PINECONE_API_KEY",
        "pcsk_5MgxE2_SvtRBE7ARYHwcVd5S5ucZEucguxrL86BCdEovgadhSFoHqDE3CmKVP5nVNRW4cm"
    )
    INDEX_NAME = "multilingual-text"
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    # 🔥 Choose your LLM provider
    # Options: "ollama" or "gemini"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

    # Default Ollama model
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")

    # Google Gemini setup
    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        "AIzaSyBw_vv1SHpPSjd_14RDbNyLolPNl5kkrIs"  # ⚠️ Replace or use env var
    )
    GEMINI_MODEL = "gemini-2.5-flash"

# ✅ Set environment
os.environ["PINECONE_API_KEY"] = Settings.PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = Settings.GEMINI_API_KEY

settings = Settings()
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

