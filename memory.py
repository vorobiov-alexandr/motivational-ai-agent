
import json

class Memory:
    def __init__(self):
        self.log = []

    def log_step(self, step, goal_name, progress_delta):
        self.log.append({
            "step": step,
            "goal": goal_name,
            "progress_delta": progress_delta
        })

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2)
