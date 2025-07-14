
import random

class MotivationModel:
    def __init__(self):
        self.mood = 1.0

    def select_goal(self, goals):
        if not goals:
            return None
        weighted_goals = [(g, g.priority * random.uniform(0.8, 1.2) * self.mood) for g in goals]
        return max(weighted_goals, key=lambda x: x[1])[0]

    def evaluate_progress(self, goal):
        return random.uniform(0.05, 0.2) * self.mood
