
from motivation import MotivationModel
from goal import GoalManager
from memory import Memory

class AIAgent:
    def __init__(self):
        self.motivation = MotivationModel()
        self.goals = GoalManager()
        self.memory = Memory()
        self.step_counter = 0

    def run_step(self):
        active_goals = self.goals.get_active_goals()
        if not active_goals:
            return
        selected_goal = self.motivation.select_goal(active_goals)
        progress = self.motivation.evaluate_progress(selected_goal)
        selected_goal.progress += progress
        self.memory.log_step(self.step_counter, selected_goal.name, progress)
        self.step_counter += 1
