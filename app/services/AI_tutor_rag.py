import openai
from typing import List, Dict, Any
from app.core.config import settings
from app.utils.pinecone_indexer import query as pinecone_query


openai.api_key= settings.openai_api_key

SYSTEM_PROMPT= ("You are Medical AI, an evidence-based tutoring assistant. "
"Do not provide diagnoses or clinical treatment directions. If the user requests diagnosis or emergency advice, refuse and recommend a clinician. "
"Cite any factual claims with the provided source metadata in square brackets."
)

def retrieve_contexts(question: str, top_k: int= None) -> List[Dict[str, Any]]:
    result= pinecone_query(question, top_k= top_k)
    matches= result.get("matches", []) if isinstance(result, dict) else getattr(result, "matches", [])
    contexts= []

    for m in matches:
        meta= m.get("metadata") or m.metadata
        contexts.append({
            "id": m.get("id") or m.id,
            "score": m.get("score") or m.score,
            "title": meta.get("title"),
            "doc_id": meta.get("doc_id"),
            "chunk_index": meta.get("chunk_index"),
            "text": (meta.get("text_snippet") or meta.get("text"))
        })
    
    return contexts

def build_prompt(user_query: str, contexts: List[Dict[str, Any]], user_profile: Dict= None, session_history: List[Dict]= None) -> str:
    parts= [SYSTEM_PROMPT, "\n\nCONTEXT:\n"]
    for i, c in enumerate(contexts):
        parts.append(f"[{i+1}]{c['title']}(doc:{c['doc_id']} chunk:{c['chunk_index']})\n{c['text']}\n---\n")
    

    if user_profile:
        parts.append("\n USER PROFILE: \n")
        for m in session_history[-6:]:
            parts.append(f"{m['role']}: {m['text']}\n")
        
    parts.append("\nUSER QUERY:\n" + user_query + "\n\nINSTRUCTIONS:\nAnswer concisely (<= 300 words). Use the provided context to support factual claims and cite by context number like [1]. If there is insufficient evidence, say 'I don't have a reliable source in the materials provided.'\n")
    return "".join(parts)


def call_llm(promt: str, temperature: float= 0.1, max_tokens: int=600)-> str:
    resp= openai.ChatCompletion.create(
        model= settings.llm_model,
        messages= [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        temperature= temperature,
        max_tokens= max_tokens
    )

    return resp["choices"][0]["message"]["content"]