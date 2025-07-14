
class Goal:
    def __init__(self, name, priority=1.0, progress=0.0):
        self.name = name
        self.priority = priority
        self.progress = progress

    def is_completed(self):
        return self.progress >= 1.0

class GoalManager:
    def __init__(self):
        self.goals = []

    def add_goal(self, goal):
        self.goals.append(goal)

    def get_active_goals(self):
        return [g for g in self.goals if not g.is_completed()]
