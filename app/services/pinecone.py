from pinecone import Pinecone, ServerlessSpec
import uuid
api_key="pcsk_5MgxE2_SvtRBE7ARYHwcVd5S5ucZEucguxrL86BCdEovgadhSFoHqDE3CmKVP5nVNRW4cm" 

pc= Pinecone(api_key=api_key)
index_name= "multilingual-text"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        index_name, 
        dimension= 384,
        metric='cosine',
        spec= ServerlessSpec(cloud="aws", region= "us-east-1")
        )

index= pc.Index(index_name)

def store_embeddings(chunks, embeddings,doc_id= None, max_metadata_length=3000):
    """
    Stores text chunks and their embeddings safely in Pinecone,
    ensuring metadata never exceeds 40 KB per vector.
    """
    if not doc_id:
        doc_id = str (uuid.uuid4())
    
    vectors =[]
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        safe_text = chunk[:max_metadata_length]
        vector_id = f"{doc_id}_chunk_{i}"
        vectors.append((
            vector_id,
            emb.tolist(),
            {
                "text": safe_text,
                "doc_id": doc_id,
                "chunk_index":i
            }
        ))

    index.upsert(vectors= vectors)
    print(f"Stored {len(vectors)} vectors safely in Pinecone")
    return len(vectors)