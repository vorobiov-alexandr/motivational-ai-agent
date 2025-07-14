from goal import Goal

class GoalsManager:
    def __init__(self):
        self.goals = []

    def add_goal(self, goal: Goal):
        self.goals.append(goal)

    def get_top_goal(self):
        if not self.goals:
            return None
        # Возвращаем цель с максимальным приоритетом и наименьшим прогрессом
        return max(self.goals, key=lambda g: g.priority * (1 - g.progress))

    def get_active_goals(self):
        return [g for g in self.goals if g.progress < 1.0]
