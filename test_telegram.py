from hermes.connectors.telegram import TelegramConnector
from hermes import KanbanBoard, Task

# test sending a simple message
telegram = TelegramConnector()
telegram.send("🚀 CrowdWisdom Ads Agent is starting!")

# test sending kanban status
kanban = KanbanBoard()
kanban.add_task(Task(type="scrape_ads", payload={}))
kanban.add_task(Task(type="write_script", payload={}))
telegram.send_kanban(kanban)

print("✅ Telegram test complete — check your Telegram app!")