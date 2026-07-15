import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramConnector:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str):
        # sends a message to your telegram chat
        try:
            response = requests.post(self.base_url, json={
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            })
            if response.status_code == 200:
                print(f"📨 [TELEGRAM] Sent: {message}")
            else:
                print(f"⚠️  [TELEGRAM] Failed: {response.text}")
        except Exception as e:
            print(f"⚠️  [TELEGRAM] Error: {e}")

    def send_kanban(self, kanban):
        # sends the current kanban board status to telegram
        message = (
            f"📊 <b>KANBAN UPDATE</b>\n"
            f"✅ Done: {len(kanban.done)}\n"
            f"⚙️ In Progress: {len(kanban.in_progress)}\n"
            f"📋 Todo: {len(kanban.todo)}\n"
            f"❌ Failed: {len(kanban.failed)}"
        )
        self.send(message)