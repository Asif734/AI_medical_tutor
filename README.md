1. Copy .env.example to .env and fill keys (OpenAI + Pinecone + index name).
2. pip install -r requirements.txt
3. Prepare PDFs in ./data/pdfs
4. python scripts/index_pdfs.py # indexes documents into Pinecone
5. uvicorn app.main:app --reload --port 8000
6. POST /ai/chat with {"user_id":"u1","message":"Explain the pericardium"}



### ENV file
OPENAI_API_KEY=

PINECONE_API_KEY=
PINECONE_ENV=us-west1-gcp
PINECONE_INDEX=medical-tutor-v1
PINECONE_NAMESPACE= medical
MAX_CONTEXT_TOKENS= 3000
EMBED_MODEL= text-embedding-3-small
LLM_MODEL=gpt-4o-mini
PORT= 8000