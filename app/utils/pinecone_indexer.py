import os 
import openai 
import pinecone 
from typing import Dict, List 
from .chunker import chunk_text
from app.core.config import settings


openai.api_key= settings.openai_api_key

#Intitialize Pinecone
pinecone.init(api_key= settings.pinecone_api_key, environment= settings.pinecone_env)
index= pinecone.Index(settings.pinecone_index)

EMBED_MODEL= settings.embed_model

def embed_text(text: str) -> List[float]:
    #use openai embeddings
    resp= openai.Embedding.create(model= EMBED_MODEL, input= text)
    return resp["data"][0]["embedding"]

def index_documents(doc_id: str, title: str, txt: str, metadata: Dict= None):
    metadata= metadata or {}
    chunks= chunk_text(text)

    vectors=[]
    for i, chunk in enumerate (chunks):
        emb= embed_text(chunk)
        meta = {**metadata, "doc_id": doc_id, "title": title, "chunk_index": i}
        vectors.append((f"{doc_id}_{i}", emb, meta))

    #upsert in batches
    batch_size= 64
    for i in range(0, len(vectors), batch_size):
        chunk_batch= vectors[i:i+batch_size]
        ids =[v[0] for v in chunk_batch]
        vecs= [v[1] for v in chunk_batch]
        metas- [v[2] for v in chunk_batch]
        index.upsert(vectors=list(zip(ids, vecs, metas)), namespace= settings.pinecone_namespace)
        

def query(query_text: str, top_k: int =None):
    top_k= top_k or settings.top_k
    q_emb= embed_text(query_text)
    res= index.query(vector= q_emb, top_k= top_k, include_metadata= True, namespace= settings.pinecone_namespace)
    return res 
