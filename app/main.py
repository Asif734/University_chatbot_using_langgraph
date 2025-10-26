from fastapi import FastAPI 
from app.routes import upload_file, query, authentication

app= FastAPI()

@app.get("/")
async def get_root():
    return "Server started Successfully"

app.include_router(authentication.router, tags=["Authentication"])
app.include_router(upload_file.router, tags=["Upload file"])
app.include_router(query.router, tags=["Query"])