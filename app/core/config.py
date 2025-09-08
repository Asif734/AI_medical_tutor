from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key:str
    pinecone_env: str
    pinecone_index: str= "medical-tutor-v1"
    pinecone_namespace: str= "medical"
    embed_model: str= "text-embedding-3-small"
    llm_model: str= "gpt-40-mini"
    max_context_tokens: int= 3000
    top_k: int= 6
    port: int= 8000


    class Config:
        env_file= ".env"

settings= Settings()