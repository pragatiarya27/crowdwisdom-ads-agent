from hermes.kanban import KanbanBoard
from hermes.skill import BaseSkill

class BaseAgent:
    def __init__(self, name: str, kanban: KanbanBoard, skills: list[BaseSkill], task_types: list[str]):
        self.name = name
        self.kanban = kanban
        self.skills = {skill.name: skill for skill in skills}  # dict by name
        self.task_types = task_types   # which task types this agent handles

    def get_skill(self, name: str) -> BaseSkill:
        return self.skills.get(name)

    def run(self):
        # pick next task this agent can handle
        for task_type in self.task_types:
            task = self.kanban.get_next_task(task_type)
            if task:
                task.agent = self.name
                self.kanban.start_task(task)
                try:
                    result = self.handle(task)
                    self.kanban.complete_task(task, result)
                except Exception as e:
                    self.kanban.fail_task(task, str(e))
                return  # one task per loop cycle

    def handle(self, task) -> dict:
        raise NotImplementedError("Each agent must implement handle()")

    def __repr__(self):
        return f"Agent({self.name})"