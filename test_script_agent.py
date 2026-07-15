import json
from hermes import KanbanBoard, Task, AgentLoop
from hermes.connectors.telegram import TelegramConnector
from agents.script_agent import ScriptAgent

telegram = TelegramConnector()
kanban = KanbanBoard()

# add tasks
kanban.add_task(Task(type="index_pdfs", payload={}))
kanban.add_task(Task(type="write_scripts", payload={}))

# create agent
script_agent = ScriptAgent(kanban=kanban)

# run
telegram.send("🚀 Script Agent starting!")
loop = AgentLoop(kanban=kanban, agents=[script_agent], interval=2)
loop.start()

# show results
print(kanban.summary())
telegram.send_kanban(kanban)

# print scripts
with open("data/scripts_output.json", "r") as f:
    scripts = json.load(f)

for i, script in enumerate(scripts):
    print(f"\n{'='*50}")
    print(f"Script {i+1} — {script['type'].upper()}")
    print(f"{'='*50}")
    print(script['script'])

print("\n✅ Script Agent complete!")