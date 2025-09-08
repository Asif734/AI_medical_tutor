from fastapi import FastAPI, HTTPException, APIRouter
from app.schemas.models import ChatRequest, ChatResponse
from app.services.AI_tutor_rag import retrieve_contexts, build_prompt, call_llm
from app.core.config import settings

router= APIRouter(title= "Medical AI tutor -Rag")

@router.post("ai/chat", response_model= ChatResponse)
def mai_chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code= 400, details="Empty message")
    

    #1.Retrive
    contexts= retrieve_contexts(req.message, top_k= settings.top_k)

    #2. Optional: load user profile / session history (stubbed)
    user_profile= {"enrolled course": "medical anatomy", "recent_quiz_avg":"68%"}
    session_history= []

    #3. build prompt
    prompt= build_prompt(req.message, contexts, user_profile= user_profile, session_history= session_history)

    #4. LLM call
    reply= call_llm(prompt)

    #5. Format sources
    sources= []
    for i, c in enumerate(contexts):
        sources.append({"id": c["doc_id"], "title": c["title"],"snippet": c["text"][:400], "score": c["score"] })
    
    return ChatResponse(reply= reply, sources= sources, actions =[], confidence= 0.9)

