from fastapi import FastAPI
from pydantic import BaseModel
from artus_brain import ArTusBrain

app = FastAPI()

# ===============================
# DATA MODEL
# ===============================
class Query(BaseModel):
    question: str

# ===============================
# INITIALIZE REAL ARTUS BRAIN
# ===============================
brain = ArTusBrain()

# ===============================
# API ENDPOINT
# ===============================
@app.post("/ask-artus")
def ask_artus(q: Query):
    response = brain.process(q.question)

    return {
        "response": response,
        "memory_size": len(brain.memory)
    }

# ===============================
# HEALTH CHECK
# ===============================
@app.get("/")
def root():
    return {"status": "ArTus API is running"}