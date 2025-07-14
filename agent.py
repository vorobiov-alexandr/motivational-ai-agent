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

    def fetch_google_search(self, query):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/103.0.0.0 Safari/537.36"
            }
            response = requests.get(f"https://www.google.com/search?q={query}", headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                for g in soup.find_all('div', class_='tF2Cxc')[:3]:
                    title = g.find('h3')
                    link = g.find('a')['href']
                    if title and link:
                        results.append(f"{title.get_text()} - {link}")
                return "\n".join(results) if results else "Ничего не найдено"
            else:
                return "Ошибка запроса к Google"
        except Exception as e:
            return f"Ошибка: {e}"

    def run_step(self):
        goal = self.goals.get_top_goal()
        if not goal:
            return

        info = self.fetch_google_search(goal.name)

        progress_delta = 0.1
        goal.progress = min(1.0, goal.progress + progress_delta)

        log_entry = {
            "step": len(self.memory.log) + 1,
            "goal": goal.name,
            "progress_delta": progress_delta,
            "motivation": self.motivation.level,
            "mood": self.motivation.mood,
            "info": info,
            "source": f"Google Search: {goal.name}"
        }
        self.memory.log.append(log_entry)
