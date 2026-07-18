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
--text
project/
├── hermes/                          # Custom Hermes Framework
│   ├── task.py                      # Task dataclass
│   ├── kanban.py                    # KanbanBoard
│   ├── skill.py                     # BaseSkill
│   ├── agent.py                     # BaseAgent
│   ├── loop.py                      # AgentLoop
│   └── connectors/
│       └── telegram.py              # Telegram connector
│
├── agents/
│   ├── ads_manager_agent.py         # Agent 1
│   ├── script_agent.py              # Agent 2
│   └── video_agent.py               # Agent 3
│
├── skills/
│   ├── apify_scraper_skill.py
│   ├── pain_extractor_skill.py
│   ├── rag_skill.py
│   ├── script_writer_skill.py
│   └── video_generator_skill.py
│
├── data/
│   ├── ads_results.json
│   ├── pain_concepts.json
│   ├── scripts_output.json
│   └── crowdwisdom_data_1.json
│
├── output/
│   └── videos/                      # Generated MP4 advertisements
│
├── main.py                          # Runs the complete multi-agent pipeline
└── config.py                        # Configuration and API keys

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
OPENROUTER_API_KEY
APIFY_API_TOKEN
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
PEXELS_API_KEY
ELEVENLABS_API_KEY
PDF_DATA_DIR=data/
OUTPUT_DIR=output/videos/
CHROMA_DB_DIR=data/chroma_db/
```

### 6. Run the full pipeline
```bash
python main.py
```


## 📊 Pipeline FlowAdsManagerAgent

AdsManagerAgent
├── Scrapes advertisements from the Meta Ads Library using Apify
├── Extracts customer pain points using an LLM
└── Saves the output to:
    ├── data/ads_results.json
    └── data/pain_concepts.json

ScriptAgent
├── Indexes CrowdWisdom data using RAG (ChromaDB)
├── Generates three advertisement scripts:
│   ├── Pain-Based Ad
│   │   └── Focuses on trader pain points
│   ├── Data-Based Ad
│   │   └── Highlights unique CrowdWisdom insights
│   └── Crowd Wisdom Ad
│       └── Emphasizes collective market intelligence
└── Saves the output to:
    └── data/scripts_output.json

VideoAgent
├── Parses generated scripts into scenes
├── Creates HTML-based video compositions
├── Renders videos into MP4 format using HyperFrames
└── Saves the generated videos to:
    └── output/videos/
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

## 📚 Data Sources

### CrowdWisdom Proprietary Data
- `data/crowdwisdom_data_1.json` — Real trading signals and market analysis
- `data/crowdwisdom_data_2.json` — Crowd sentiment and trading insights

### Meta Ads Library
- Scraped via Apify: `apify/facebook-ads-scraper`
- Query: "trading signals stock market crowd wisdom"

### Reference Videos (Style Inspiration)
- https://www.youtube.com/watch?v=UBvrPGMtK5g
- https://www.youtube.com/watch?v=JFMxDgmW8cw
- https://www.youtube.com/watch?v=8nFTkjPk80k
- https://www.youtube.com/watch?v=bpM9D1kQaAs
- https://www.youtube.com/watch?v=g-qW8fQimyg
- https://www.youtube.com/watch?v=vqFUuLO06qc

### Alternative Video Tools (Evaluated)
- https://github.com/baldiga/headless-studio
- https://github.com/OpenCut-app/OpenCut
- https://github.com/calesthio/OpenMontage

---

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

*Built for CrowdWisdomTrading.com internship assessment by Pragati Arya*
Save then run:

bash
git add .
git commit -m "Update README with complete documentation and data sources"
git push origin main






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
