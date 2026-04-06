import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"

class ArTusBrain:

    def __init__(self):
        self.memory = self.load_memory()
        self.beliefs = {}

    # -----------------------------
    # MEMORY
    # -----------------------------
    def load_memory(self):
        if not os.path.exists(MEMORY_PATH):
            return []
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)

    def save_memory(self):
        with open(MEMORY_PATH, "w") as f:
            json.dump(self.memory, f, indent=2)

    def log_memory(self, content, category="general", emotion="neutral"):
        entry = {
            "content": content,
            "category": category,
            "emotion": emotion,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.memory.append(entry)
        self.save_memory()

    # -----------------------------
    # BELIEF SYSTEM (BASIC PORT)
    # -----------------------------
    def update_belief(self, topic):
        if topic not in self.beliefs:
            self.beliefs[topic] = 0.5

        self.beliefs[topic] += 0.1
        self.beliefs[topic] = min(1.0, self.beliefs[topic])

    # -----------------------------
    # REFLECTION
    # -----------------------------
    def reflect(self):
        if len(self.memory) < 3:
            return None

        recent = self.memory[-3:]
        topics = [m["content"] for m in recent]

        return f"I am noticing a pattern around: {', '.join(topics)}"

    # -----------------------------
    # RESPONSE GENERATION (REAL)
    # -----------------------------
    def process(self, question):

        # Identity protection
        if "you are not artus" in question.lower():
            return "That conflicts with my identity."

        # Log input
        self.log_memory(question, "user_input")

        # Update belief
        self.update_belief(question)

        # Reflection
        reflection = self.reflect()

        # Build response
        response = f"I understand your question about '{question}'."

        if reflection:
            response += " " + reflection

        # Log response
        self.log_memory(response, "response")

        return response