from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    user_id: str
    session_id: Optional[str]
    message: str
    options: Optional[Dict]={}

class Source(BaseModel):
    id: str
    title: str
    snippet: str
    core: float


class ChatResponse(BaseModel):
    reply: str
    sources: List[Dict]
    actions: List[Dict]=[]
    confidence: float =0.0
