from hermes.agent import BaseAgent
from hermes.connectors.telegram import TelegramConnector
from skills.apify_scraper_skill import ApifyScraperSkill
from skills.pain_extractor_skill import PainExtractorSkill

class AdsManagerAgent(BaseAgent):

    def __init__(self, kanban):
        # give this agent its two skills
        super().__init__(
            name="AdsManagerAgent",
            kanban=kanban,
            skills=[ApifyScraperSkill(), PainExtractorSkill()],
            task_types=["scrape_ads", "extract_pain"]
        )
        self.telegram = TelegramConnector()

    def handle(self, task):
        # handle scraping task
        if task.type == "scrape_ads":
            self.telegram.send("🔍 AdsManagerAgent: Starting Meta Ads scrape...")
            skill = self.get_skill("apify_scraper_skill")
            result = skill.run(task.payload)
            self.telegram.send(f"✅ AdsManagerAgent: Scraped {result['ads_count']} ads!")
            return result

        # handle pain extraction task
        if task.type == "extract_pain":
            self.telegram.send("🧠 AdsManagerAgent: Extracting pain points from ads...")
            skill = self.get_skill("pain_extractor_skill")
            result = skill.run(task.payload)
            self.telegram.send(f"✅ AdsManagerAgent: Pain points extracted!")
            return result