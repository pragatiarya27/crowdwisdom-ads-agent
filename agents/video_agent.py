import json
from hermes.agent import BaseAgent
from hermes.connectors.telegram import TelegramConnector
from skills.video_generator_skill import VideoGeneratorSkill

class VideoAgent(BaseAgent):

    def __init__(self, kanban):
        super().__init__(
            name="VideoAgent",
            kanban=kanban,
            skills=[VideoGeneratorSkill()],
            task_types=["generate_videos"]
        )
        self.telegram = TelegramConnector()

    def handle(self, task):
        if task.type == "generate_videos":
            self.telegram.send("🎬 VideoAgent: Starting video generation...")

            # load scripts
            with open("data/scripts_output.json", "r") as f:
                scripts = json.load(f)

            skill = self.get_skill("video_generator_skill")
            result = skill.run({"scripts": scripts})

            self.telegram.send(f"✅ VideoAgent: {result['count']} videos generated!")
            return result