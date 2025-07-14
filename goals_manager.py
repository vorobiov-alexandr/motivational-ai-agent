class GoalsManager:
    def __init__(self):
        self.goals = []

    def add_goal(self, goal):
        self.goals.append(goal)

    def get_top_goal(self):
        if not self.goals:
            return None
        active_goals = [g for g in self.goals if g.progress < 1.0]
        if not active_goals:
            return None
        return max(active_goals, key=lambda g: g.priority)

    def get_active_goals(self):
        return [g for g in self.goals if g.progress < 1.0]