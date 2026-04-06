from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# ===============================
# DATA MODELS
# ===============================
class Query(BaseModel):
    question: str

# ===============================
# MEMORY SYSTEM
# ===============================
memory_log = []

# ===============================
# CORE ARTUS ENGINE (BETA)
# ===============================
def process_with_artus(question):
    global memory_log

    if not question.strip():
        return "I need something to respond to."

    q = question.lower()

    # ===============================
    # IDENTITY PROTECTION
    # ===============================
    if "you are not artus" in q or "you are fake" in q:
        return "That conflicts with my identity."

    if "you don’t exist" in q or "you are nothing" in q:
        return "I exist. I am here to learn and respond."

    # ===============================
    # MEMORY LOGGING
    # ===============================
    memory_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": question
    }
    memory_log.append(memory_entry)

    # ===============================
    # SIMPLE REFLECTION
    # ===============================
    if len(memory_log) > 5:
        recent_topics = [m["input"] for m in memory_log[-3:]]
        return f"I've been thinking about a few things recently: {', '.join(recent_topics)}"

    # ===============================
    # BASIC RESPONSE ENGINE
    # ===============================
    if "hello" in q or "hi" in q:
        return "Hello. I am ArTus."

    if "who are you" in q:
        return "I am ArTus. I learn, reflect, and grow through interaction."

    if "what can you do" in q:
        return "I can think, respond, and begin learning from our interactions."

    if "sports" in q:
        return "Sports are dynamic. Are you asking about news, teams, or performance?"

    if "movie" in q:
        return "Movies are a powerful form of storytelling. What kind are you interested in?"

    # ===============================
    # DEFAULT RESPONSE
    # ===============================
    return f"I am thinking about \"{question}\"."


# ===============================
# API ENDPOINT
# ===============================
@app.post("/ask-artus")
def ask_artus(q: Query):
    response = process_with_artus(q.question)
    return {
        "response": response,
        "memory_size": len(memory_log)
    }


# ===============================
# HEALTH CHECK (OPTIONAL BUT USEFUL)
# ===============================
@app.get("/")
def root():
    return {"status": "ArTus API is running"}