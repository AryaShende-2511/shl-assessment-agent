from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent.router import detect_intent
from retrieval.search import search_catalog

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "SHL Assessment Agent API is running",
        "health": "/health",
        "docs": "/docs"
    }


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):

    user_messages = []

    for m in req.messages:
        if m.role == "user":
            user_messages.append(m.content)

    user_msg = " ".join(user_messages)
    intent = detect_intent(req.messages)
    print("Intent =", intent)
    print("User message =", user_msg)

    
    # Refuse
    # -------------------
    # -------------------
    # -------------------
    # Refine
    # -------------------

    if intent == "refine":

        results = search_catalog(user_msg, top_k=5)

        recs = []

        for r in results:
            recs.append({
                "name": r["name"],
                "url": r.get("url", r.get("link")),
                "test_type": ", ".join(r.get("keys", []))
            })

        return {
            "reply": "I've updated the recommendations based on your new requirements.",
            "recommendations": recs,
            "end_of_conversation": True
        }
    # -------------------
    # Refuse
    # -------------------
    if intent == "refuse":

        return {
            "reply": "I can only help with SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------
    # Clarify
    # -------------------

    if intent == "clarify":

        return {
            "reply": "Sure! Could you tell me the role, experience level, and any skills or personality traits you want to assess?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------
    # Recommend
    # -------------------

    if intent == "recommend":

        results = search_catalog(user_msg, top_k=5)

        recs = []

        for r in results:
            recs.append({
                "name": r["name"],
                "url": r.get("url", r.get("link")),
                "test_type": ", ".join(r.get("keys", []))
            })

        return {
            "reply": f"I found {len(recs)} SHL assessments matching your requirement.",
            "recommendations": recs,
            "end_of_conversation": True
        }

    # -------------------
    # Compare
    # -------------------

    if intent == "compare":

        results = search_catalog(user_msg, top_k=2)

        if len(results) < 2:
            return {
                "reply": "I couldn't identify two SHL assessments to compare.",
                "recommendations": [],
                "end_of_conversation": False
            }

        a = results[0]
        b = results[1]

        reply = f"""
**{a['name']}**

{a.get('description', '')}

---

**{b['name']}**

{b.get('description', '')}
"""

        return {
            "reply": reply,
            "recommendations": [
                {
                    "name": a["name"],
                    "url": a.get("url", a.get("link")),
                    "test_type": ", ".join(a.get("keys", []))
                },
                {
                    "name": b["name"],
                    "url": b.get("url", b.get("link")),
                    "test_type": ", ".join(b.get("keys", []))
                }
            ],
            "end_of_conversation": True
        }

    # -------------------
    # Default
    # -------------------

    return {
        "reply": "Please tell me more about your hiring requirements.",
        "recommendations": [],
        "end_of_conversation": False
    }