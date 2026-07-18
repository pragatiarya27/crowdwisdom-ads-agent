# crowdwisdom-ads-agent
# CrowdWisdom Trading Video Ads Agent 🚀

An AI-powered multi-agent pipeline that automatically generates video ads for [CrowdWisdomTrading.com](https://crowdwisdomtrading.com) using the Hermes agent framework.

---

## 🏗️ Architecture

Built with a custom **Hermes Framework** using Kanban-style task management:
KanbanBoard → [TODO → IN_PROGRESS → DONE → FAILED]
↓
AgentLoop → runs agents in cycles until all tasks complete
↓
Agents → pick tasks → run skills → update board → notify Telegram
### 3 Agents, 5 Skills

| Agent | Skills | Output |
|-------|--------|--------|
| AdsManagerAgent | ApifyScraperSkill, PainExtractorSkill | ads_results.json, pain_concepts.json |
| ScriptAgent | RAGSkill, ScriptWriterSkill | scripts_output.json |
| VideoAgent | VideoGeneratorSkill | 3 MP4 video ads |

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Framework:** Hermes (custom Kanban agent framework)
- **LLM Provider:** OpenRouter (openrouter/free model)
- **Scraping:** Apify — Facebook Ads Library Scraper
- **RAG:** ChromaDB + hash-based embeddings- **Video Generation:** HyperFrames (npx hyperframes render)
- **Notifications:** Telegram Bot API

---

## 📁 Project Structurecrowdwisdom-ads-agent/
├── hermes/                    # Custom Hermes Framework
│   ├── task.py               # Task dataclass
│   ├── kanban.py             # KanbanBoard
│   ├── skill.py              # BaseSkill
│   ├── agent.py              # BaseAgent
│   ├── loop.py               # AgentLoop
│   └── connectors/
│       └── telegram.py       # Telegram connector
├── agents/
│   ├── ads_manager_agent.py  # Agent 1
│   ├── script_agent.py       # Agent 2
│   └── video_agent.py        # Agent 3
├── skills/
│   ├── apify_scraper_skill.py
│   ├── pain_extractor_skill.py
│   ├── rag_skill.py
│   ├── script_writer_skill.py
│   └── video_generator_skill.py
├── data/
│   ├── ads_results.json
│   ├── pain_concepts.json
│   ├── scripts_output.json
│   └── crowdwisdom_data_1.json
├── output/videos/            # Generated MP4 ads
├── main.py                   # Run full pipeline
└── config.py                 # API keys config---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/pragatiarya27/crowdwisdom-ads-agent.git
cd crowdwisdom-ads-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node.js dependencies
```bash
npm install -g npx
```

### 5. Create `.env` file
```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
APIFY_API_TOKEN=YOUR_APIFY_TOKEN
TELEGRAM_BOT_TOKEN=8853452578:AAEeLqGTCuEikEGN1vzv5SuZbyQnZGiagv8
TELEGRAM_CHAT_ID=6646531304
PEXELS_API_KEY=8xD4lM5e1ZF2PspkJzCt3VX3rnwqbt3L0ML4hiWMm46uxGGO7np8nRFG
ELEVENLABS_API_KEY=sk_fdc3516046803a03664cc5171622a72c51ededa0c6c095ff
PDF_DATA_DIR=data/
OUTPUT_DIR=output/videos/
CHROMA_DB_DIR=data/chroma_db/
```

### 6. Run the full pipeline
```bash
python main.py
```

---
## 🔑 OPENROUTER_API_KEY

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
## 🔑 APIFY Token
apify_api_p55KuiVkchimbFtNp3Ba3lLtKcvA3g4mpsln

---

## 📊 Pipeline FlowAdsManagerAgent
1. AdsManagerAgent
  └── Scrapes Meta Ads Library via Apify
  └── Extracts pain points using LLM
  └── Saves → ads_results.json, pain_concepts.json
2. ScriptAgent
  └── Indexes CrowdWisdom data via RAG (ChromaDB)
  └── Generates 3 ad scripts:
  ├── pain_based    — trader pain points
  ├── data_based    — unique CrowdWisdom data
  └── crowd_wisdom  — crowd intelligence angle
  └── Saves → scripts_output.json
3. VideoAgent
  └── Parses scripts into scenes
  └── Generates HTML compositions
  └── Renders via HyperFrames → MP4 videos
  └── Saves → output/videos/
---

## 🎬 Video Output

3 x 30-second MP4 video ads generated:
- `output/videos/ad_pain_based_1/renders/`
- `output/videos/ad_data_based_2/renders/`
- `output/videos/ad_crowd_wisdom_3/renders/`

---

## 📱 Telegram Integration

The bot sends live updates at every pipeline step:
- Task started/completed
- Kanban board status
- Video generation progress

Bot: [@CrowdWisdomAdsBot](https://t.me/CrowdWisdomAdsbot)

---

## 🧪 Individual Tests

## 🧪 Individual Tests

```bash
python test_hermen.py        # Test Hermes framework
python test_telegram.py      # Test Telegram connector
python test_ads_manager.py   # Test Ads Manager Agent
python test_script_agent.py  # Test Script Agent - generates 3 ad scripts
python test_script2.py       # Test Script 2 - prints data_based script content
python test_video_agent.py   # Test Video Agent - generates 3 MP4 videos
```

---

## 📝 Evaluation Criteria Met

- ✅ Kanban board with todo/in_progress/done/failed columns
- ✅ Agent loops running tasks in cycles
- ✅ Skills pattern (BaseSkill → concrete skills)
- ✅ Telegram live updates during pipeline
- ✅ HyperFrames video generation
- ✅ Apify Meta Ads scraping
- ✅ RAG over CrowdWisdom proprietary data
- ✅ OpenRouter LLM integration

---

*Built for CrowdWisdomTrading.com internship assessment*