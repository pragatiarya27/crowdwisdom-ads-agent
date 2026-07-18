# crowdwisdom-ads-agent

\# CrowdWisdom Trading Video Ads Agent 🚀



An AI-powered multi-agent pipeline that automatically generates video ads for \[CrowdWisdomTrading.com](https://crowdwisdomtrading.com) using the Hermes agent framework.



\---



\## 🏗️ Architecture



Built with a custom \*\*Hermes Framework\*\* using Kanban-style task management:

KanbanBoard → \[TODO → IN\_PROGRESS → DONE → FAILED]

↓

AgentLoop → runs agents in cycles until all tasks complete

↓

Agents → pick tasks → run skills → update board → notify Telegram

\### 3 Agents, 5 Skills



| Agent | Skills | Output |

|-------|--------|--------|

| AdsManagerAgent | ApifyScraperSkill, PainExtractorSkill | ads\_results.json, pain\_concepts.json |

| ScriptAgent | RAGSkill, ScriptWriterSkill | scripts\_output.json |

| VideoAgent | VideoGeneratorSkill | 3 MP4 video ads |



\---



\## 🛠️ Tech Stack



\- \*\*Language:\*\* Python 3.12

\- \*\*Framework:\*\* Hermes (custom Kanban agent framework)

\- \*\*LLM Provider:\*\* OpenRouter (openrouter/free model)

\- \*\*Scraping:\*\* Apify — Facebook Ads Library Scraper

\- \*\*RAG:\*\* ChromaDB + hash-based embeddings- \*\*Video Generation:\*\* HyperFrames (npx hyperframes render)

\- \*\*Notifications:\*\* Telegram Bot API



\---



\## 📁 Project Structurecrowdwisdom-ads-agent/

├── hermes/                    # Custom Hermes Framework

│   ├── task.py               # Task dataclass

│   ├── kanban.py             # KanbanBoard

│   ├── skill.py              # BaseSkill

│   ├── agent.py              # BaseAgent

│   ├── loop.py               # AgentLoop

│   └── connectors/

│       └── telegram.py       # Telegram connector

├── agents/

│   ├── ads\_manager\_agent.py  # Agent 1

│   ├── script\_agent.py       # Agent 2

│   └── video\_agent.py        # Agent 3

├── skills/

│   ├── apify\_scraper\_skill.py

│   ├── pain\_extractor\_skill.py

│   ├── rag\_skill.py

│   ├── script\_writer\_skill.py

│   └── video\_generator\_skill.py

├── data/

│   ├── ads\_results.json

│   ├── pain\_concepts.json

│   ├── scripts\_output.json

│   └── crowdwisdom\_data\_1.json

├── output/videos/            # Generated MP4 ads

├── main.py                   # Run full pipeline

└── config.py                 # API keys config---



\## ⚙️ Setup



\### 1. Clone the repo

```bash

git clone https://github.com/pragatiarya27/crowdwisdom-ads-agent.git

cd crowdwisdom-ads-agent

```



\### 2. Create virtual environment

```bash

python -m venv venv

venv\\Scripts\\activate

```



\### 3. Install dependencies

```bash

pip install -r requirements.txt

```



\### 4. Install Node.js dependencies

```bash

npm install -g npx

```



\### 5. Create `.env` file

```env

OPENROUTER\_API\_KEY=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

APIFY\_API\_TOKEN=apify\_api\_p55KuiVkchimbFtNp3Ba3lLtKcvA3g4mpsln

TELEGRAM\_BOT\_TOKEN=8853452578:AAEeLqGTCuEikEGN1vzv5SuZbyQnZGiagv8

TELEGRAM\_CHAT\_ID=6646531304

PEXELS\_API\_KEY=8xD4lM5e1ZF2PspkJzCt3VX3rnwqbt3L0ML4hiWMm46uxGGO7np8nRFG

ELEVENLABS\_API\_KEY=sk\_fdc3516046803a03664cc5171622a72c51ededa0c6c095ff

PDF\_DATA\_DIR=data/

OUTPUT\_DIR=output/videos/

CHROMA\_DB\_DIR=data/chroma\_db/

```



\### 6. Run the full pipeline

```bash

python main.py

```



\---



\## 🔑 APIFY Token

apify\_api\_p55KuiVkchimbFtNp3Ba3lLtKcvA3g4mpsln



\---



\## 📊 Pipeline FlowAdsManagerAgent

1\. AdsManagerAgent

&#x20; └── Scrapes Meta Ads Library via Apify

&#x20; └── Extracts pain points using LLM

&#x20; └── Saves → ads\_results.json, pain\_concepts.json

2\. ScriptAgent

&#x20; └── Indexes CrowdWisdom data via RAG (ChromaDB)

&#x20; └── Generates 3 ad scripts:

&#x20; ├── pain\_based    — trader pain points

&#x20; ├── data\_based    — unique CrowdWisdom data

&#x20; └── crowd\_wisdom  — crowd intelligence angle

&#x20; └── Saves → scripts\_output.json

3\. VideoAgent

&#x20; └── Parses scripts into scenes

&#x20; └── Generates HTML compositions

&#x20; └── Renders via HyperFrames → MP4 videos

&#x20; └── Saves → output/videos/

\---



\## 🎬 Video Output



3 x 30-second MP4 video ads generated:

\- `output/videos/ad\_pain\_based\_1/renders/`

\- `output/videos/ad\_data\_based\_2/renders/`

\- `output/videos/ad\_crowd\_wisdom\_3/renders/`



\---



\## 📱 Telegram Integration



The bot sends live updates at every pipeline step:

\- Task started/completed

\- Kanban board status

\- Video generation progress



Bot: \[@CrowdWisdomAdsBot](https://t.me/CrowdWisdomAdsbot)



\---



\## 🧪 Individual Tests



\## 🧪 Individual Tests



```bash

python test\_hermen.py        # Test Hermes framework

python test\_telegram.py      # Test Telegram connector

python test\_ads\_manager.py   # Test Ads Manager Agent

python test\_script\_agent.py  # Test Script Agent - generates 3 ad scripts

python test\_script2.py       # Test Script 2 - prints data\_based script content

python test\_video\_agent.py   # Test Video Agent - generates 3 MP4 videos

```



\---



\## 📝 Evaluation Criteria Met



\- ✅ Kanban board with todo/in\_progress/done/failed columns

\- ✅ Agent loops running tasks in cycles

\- ✅ Skills pattern (BaseSkill → concrete skills)

\- ✅ Telegram live updates during pipeline

\- ✅ HyperFrames video generation

\- ✅ Apify Meta Ads scraping

\- ✅ RAG over CrowdWisdom proprietary data

\- ✅ OpenRouter LLM integration



\---



\*Built for CrowdWisdomTrading.com internship assessment\*

