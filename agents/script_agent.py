import json
from hermes.agent import BaseAgent
from hermes.connectors.telegram import TelegramConnector
from skills.rag_skill import RAGSkill
from skills.script_writer_skill import ScriptWriterSkill

class ScriptAgent(BaseAgent):

    def __init__(self, kanban):
        super().__init__(
            name="ScriptAgent",
            kanban=kanban,
            skills=[RAGSkill(), ScriptWriterSkill()],
            task_types=["index_pdfs", "write_scripts"]
        )
        self.telegram = TelegramConnector()

    def handle(self, task):
        if task.type == "index_pdfs":
            self.telegram.send("📄 ScriptAgent: Indexing CrowdWisdom PDFs...")
            rag = self.get_skill("rag_skill")
            result = rag.run({"query": "crowd wisdom trading statistics"})
            self.telegram.send("✅ ScriptAgent: PDFs indexed!")
            return result

        if task.type == "write_scripts":
            self.telegram.send("✍️ ScriptAgent: Writing 3 ad scripts...")

            with open("data/pain_concepts.json", "r") as f:
                concepts = json.load(f)

            rag = self.get_skill("rag_skill")
            rag.index_pdfs()
            rag_result = rag.run({"query": "crowd wisdom unique trading data statistics results"})

            writer = self.get_skill("script_writer_skill")
            result = writer.run({
                "pain_points": concepts.get("pain_points", []),
                "selling_points": concepts.get("selling_points", []),
                "rag_chunks": rag_result.get("chunks", [])
            })

            self.telegram.send("✅ ScriptAgent: 3 scripts written!")
            return result