from hermes import KanbanBoard, Task, AgentLoop
from hermes.connectors.telegram import TelegramConnector
from agents.ads_manager_agent import AdsManagerAgent

# setup
telegram = TelegramConnector()
kanban = KanbanBoard()

# add tasks to kanban board
kanban.add_task(Task(
    type="scrape_ads",
    payload={"query": "trading signals stock market crowd wisdom"}
))

kanban.add_task(Task(
    type="extract_pain",
    payload={}  # will load from ads_results.json automatically
))

# create agent
ads_agent = AdsManagerAgent(kanban=kanban)

# run the loop
telegram.send("🚀 Pipeline starting — Ads Manager Agent")
loop = AgentLoop(kanban=kanban, agents=[ads_agent], interval=2)
loop.start()

# print final kanban
print(kanban.summary())
telegram.send_kanban(kanban)
print("✅ Ads Manager Agent complete!")
print("📁 Check data/ads_results.json and data/pain_concepts.json")