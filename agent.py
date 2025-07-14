# === agent.py ===
from memory import Memory
from goals import GoalsManager
from motivation import Motivation
from google_search import google_search
import random

class AIAgent:
    def __init__(self):
        self.memory = Memory()
        self.goals = GoalsManager()
        self.motivation = Motivation()
        self.step_count = 0

    def run_step(self):
        self.step_count += 1
        goal = self.motivation.select_goal(self.goals)
        if not goal:
            return

        # Эмуляция выполнения шага
        progress_delta = min(1.0 - goal.progress, random.uniform(0.01, 0.1))
        goal.progress += progress_delta

        # Получение информации из Google по теме цели
        info_sources = google_search(goal.name)
        source_info = info_sources[0] if info_sources else "Ничего не найдено"

        # Сохранение в память
        self.memory.log_step({
            "step": self.step_count,
            "goal": goal.name,
            "progress_delta": progress_delta,
            "motivation": self.motivation.calculate_motivation(goal),
            "mood": self.motivation.mood,
            "source": source_info
        })
