from hermes import KanbanBoard, Task, AgentLoop
from hermes.connectors.telegram import TelegramConnector
from agents.video_agent import VideoAgent

telegram = TelegramConnector()
kanban = KanbanBoard()

# add video generation task
kanban.add_task(Task(
    type="generate_videos",
    payload={}
))

# create agent
video_agent = VideoAgent(kanban=kanban)

# run
telegram.send("🎬 Video Agent starting!")
loop = AgentLoop(kanban=kanban, agents=[video_agent], interval=2)
loop.start()

# show results
print(kanban.summary())
telegram.send_kanban(kanban)

# print video paths
result = kanban.done[0].result
print("\n✅ Videos generated:")
for path in result.get("video_paths", []):
    print(f"  📹 {path}")