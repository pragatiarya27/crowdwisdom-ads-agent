import time
from hermes.kanban import KanbanBoard
from hermes.agent import BaseAgent

class AgentLoop:
    def __init__(self, kanban: KanbanBoard, agents: list[BaseAgent], interval: int = 2):
        self.kanban = kanban
        self.agents = agents
        self.interval = interval   # seconds between each loop cycle

    def start(self):
        print("🚀 [LOOP] Agent loop started...\n")
        cycle = 0
        while not self.kanban.all_done():
            cycle += 1
            print(f"\n--- Loop Cycle {cycle} ---")
            for agent in self.agents:
                agent.run()
            print(self.kanban.summary())
            if not self.kanban.all_done():
                time.sleep(self.interval)

        print("\n🎉 [LOOP] All tasks complete!")