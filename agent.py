from goal import Goal
from goals_manager import GoalsManager
from motivation import MotivationSystem
from memory import Memory
import requests
from bs4 import BeautifulSoup

class AIAgent:
    def __init__(self):
        self.goals = GoalsManager()
        self.motivation = MotivationSystem()
        self.memory = Memory()

    def fetch_wikipedia_intro(self, topic):
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.select('p')
                for p in paragraphs:
                    text = p.get_text().strip()
                    if text:
                        return text
            return "Информация не найдена."
        except Exception as e:
            return f"Ошибка запроса: {e}"

    def run_step(self):
        goal = self.goals.get_top_goal()
        if not goal:
            return

        info = self.fetch_wikipedia_intro(goal.name)

        progress_delta = 0.1
        goal.progress = min(1.0, goal.progress + progress_delta)

        log_entry = {
            "step": len(self.memory.log) + 1,
            "goal": goal.name,
            "progress_delta": progress_delta,
            "motivation": self.motivation.level,
            "mood": self.motivation.mood,
            "info": info,
            "source": f"Wikipedia: {goal.name}"
        }
        self.memory.log.append(log_entry)