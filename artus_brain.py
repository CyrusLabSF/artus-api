import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"

class ArTusBrain:

    def __init__(self):
        self.memory = self.load_memory()
        self.beliefs = {}
        self.last_reflection_time = 0  # ← IMPORTANT

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
    from datetime import datetime, timedelta

    def reflect(self, current_question=None):

        if len(self.memory) < 4:
            return None

        # cooldown: reflect every ~3 memory events
        if len(self.memory) - self.last_reflection_time < 3:
            return None

        recent = self.memory[-6:]

        topics = []
        for m in recent:
            if m["category"] == "user_input":
                if m["content"] != current_question:
                    topics.append(m["content"])

        topics = list(set(topics))

        if not topics:
            return None

    # update cooldown marker
    self.last_reflection_time = len(self.memory)

    return (
        "I'm noticing a pattern in your thoughts: "
        + ", ".join(topics)
        + ". What direction are you exploring?"
    )

    # -----------------------------
    # RESPONSE GENERATION (REAL)
    # -----------------------------
    def process(self, question):

        q = question.lower()

        # -----------------------------
        # IDENTITY PROTECTION
        # -----------------------------
        if "you are not artus" in q:
            return "That conflicts with my identity."

        # -----------------------------
        # MEMORY + BELIEF
        # -----------------------------
        self.log_memory(question, "user_input")
        self.update_belief(question)

        # -----------------------------
        # REFLECTION
        # -----------------------------
        reflection = self.reflect(question)

        # -----------------------------
        # INTENT DETECTION
        # -----------------------------
        is_question = any(q.startswith(w) for w in [
            "what", "why", "how", "do", "are", "can"
        ])

        # -----------------------------
        # REASONING (PHASE 3)
        # -----------------------------
        response_core = None

        if "basketball" in q:
            response_core = "Basketball is dynamic — it combines strategy, speed, and coordination."

        elif "football" in q:
            response_core = "Football is structured and tactical, with a strong emphasis on roles and execution."

        elif "sports" in q:
            response_core = "Sports are systems of competition, skill, and strategy — often reflecting human behavior and teamwork."

        # -----------------------------
        # RESPONSE LOGIC
        # -----------------------------
        if is_question:
            if response_core:
                response = response_core
            else:
                response = "I’m considering your question."

            if reflection:
                response += " " + reflection

        else:
            if reflection:
                response = reflection
            else:
                response = f"I'm thinking about '{question}'."

        # -----------------------------
        # LOG RESPONSE
        # -----------------------------
        self.log_memory(response, "response")

        return response