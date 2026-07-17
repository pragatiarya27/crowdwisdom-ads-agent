import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Scraping
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Video Assets
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# TTS
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Paths
PDF_DATA_DIR = os.getenv("PDF_DATA_DIR", "data/")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/videos/")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "data/chroma_db/")

# LLM Settings
LLM_MODEL =  "openrouter/free"
LLM_BASE_URL = "https://openrouter.ai/api/v1"

MAX_TOKENS = 2000
