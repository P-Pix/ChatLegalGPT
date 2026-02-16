from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rag import ChatLegalRAG
from config import CORS_ORIGINS, MAX_QUESTION_CHARS

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="ChatLegalGPT API", version="0.2.0")
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = ChatLegalRAG()

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=MAX_QUESTION_CHARS)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Trop de requêtes. Réessayez plus tard."})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
@limiter.limit("30/minute")
def chat(req: ChatRequest, request: Request):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question vide.")
    answer, retrieved = rag.generate(q)
    return {"answer": answer, "retrieved": retrieved}
