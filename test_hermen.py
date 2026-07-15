from hermes import Task, KanbanBoard, BaseSkill, BaseAgent, AgentLoop

# create board
kanban = KanbanBoard()

# create a dummy task
task = Task(type="test_task", payload={"message": "hello"})
kanban.add_task(task)

# create a dummy skill
class HelloSkill(BaseSkill):
    name = "hello_skill"
    def run(self, input: dict) -> dict:
        return {"reply": f"processed: {input['message']}"}

# create a dummy agent
class HelloAgent(BaseAgent):
    def handle(self, task):
        skill = self.get_skill("hello_skill")
        return skill.run(task.payload)

# wire everything up
agent = HelloAgent(
    name="TestAgent",
    kanban=kanban,
    skills=[HelloSkill()],
    task_types=["test_task"]
)

# run the loop
loop = AgentLoop(kanban=kanban, agents=[agent])
loop.start()

# print result
print("\nResult:", kanban.done[0].result)