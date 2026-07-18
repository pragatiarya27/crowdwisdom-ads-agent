import json
from hermes import KanbanBoard, Task, AgentLoop
from hermes.connectors.telegram import TelegramConnector
from agents.ads_manager_agent import AdsManagerAgent
from agents.script_agent import ScriptAgent
from agents.video_agent import VideoAgent

def main():
    print("🚀 CrowdWisdom Trading Video Ads Agent — Starting Pipeline")
    print("="*60)

    # setup telegram and kanban
    telegram = TelegramConnector()
    kanban = KanbanBoard()

    telegram.send("🚀 CrowdWisdom Ads Pipeline Starting!\n📋 All 3 agents ready.")

    # ── PHASE 1: Ads Manager Agent ──
    print("\n📌 PHASE 1: Ads Manager Agent")
    kanban.add_task(Task(type="scrape_ads", payload={
        "query": "trading signals stock market crowd wisdom"
    }))
    kanban.add_task(Task(type="extract_pain", payload={}))

    ads_agent = AdsManagerAgent(kanban=kanban)
    loop1 = AgentLoop(kanban=kanban, agents=[ads_agent], interval=2)
    loop1.start()

    telegram.send_kanban(kanban)
    print(kanban.summary())

    # ── PHASE 2: Script Agent ──
    print("\n📌 PHASE 2: Script Agent")
    kanban.add_task(Task(type="index_pdfs", payload={}))
    kanban.add_task(Task(type="write_scripts", payload={}))

    script_agent = ScriptAgent(kanban=kanban)
    loop2 = AgentLoop(kanban=kanban, agents=[script_agent], interval=2)
    loop2.start()

    telegram.send_kanban(kanban)
    print(kanban.summary())

    # ── PHASE 3: Video Agent ──
    print("\n📌 PHASE 3: Video Agent")
    kanban.add_task(Task(type="generate_videos", payload={}))

    video_agent = VideoAgent(kanban=kanban)
    loop3 = AgentLoop(kanban=kanban, agents=[video_agent], interval=2)
    loop3.start()

    telegram.send_kanban(kanban)
    print(kanban.summary())

    # ── FINAL RESULTS ──
    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETE!")
    print("="*60)

    # print generated scripts
    try:
        with open("data/scripts_output.json", "r", encoding="utf-8") as f:
            scripts = json.load(f)
        print(f"\n📝 Generated {len(scripts)} scripts:")
        for s in scripts:
            print(f"  ✅ {s['type']}")
    except:
        pass

    # print generated videos
    done_tasks = [t for t in kanban.done if t.type == "generate_videos"]
    if done_tasks:
        videos = done_tasks[0].result.get("video_paths", [])
        print(f"\n🎬 Generated {len(videos)} videos:")
        for v in videos:
            print(f"  📹 {v}")
        telegram.send(f"🎉 Pipeline complete!\n🎬 {len(videos)} videos generated!")
    else:
        print("\n⚠️ No videos generated")

    print("\n✅ All done! Check output/videos/ for your ad videos.")

if __name__ == "__main__":
    main()