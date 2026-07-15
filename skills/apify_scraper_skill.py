import json
from apify_client import ApifyClient
from hermes.skill import BaseSkill
from config import APIFY_API_TOKEN

class ApifyScraperSkill(BaseSkill):
    name = "apify_scraper_skill"

    def run(self, input: dict) -> dict:
        print("🔍 [SCRAPER] Connecting to Apify...")
        client = ApifyClient(APIFY_API_TOKEN)

        query = input.get("query", "trading signals")
        # build meta ads library URL directly
        search_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q={query.replace(' ', '%20')}&search_type=keyword_unordered"

        print(f"🔍 [SCRAPER] Searching Meta Ads for: {query}")

        run = client.actor("apify/facebook-ads-scraper").call(
            run_input={
                "startUrls": [{"url": search_url}],
                "maxResults": 20
            }
        )

        ads = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            ads.append({
                "id": item.get("id", ""),
                "body": item.get("adArchiveID", ""),
                "page_name": item.get("pageName", ""),
                "text": str(item.get("snapshot", "")),
                "status": item.get("isActive", False)
            })

        with open("data/ads_results.json", "w") as f:
            json.dump(ads, f, indent=2)

        print(f"✅ [SCRAPER] Found {len(ads)} ads, saved to data/ads_results.json")
        return {"ads_count": len(ads), "ads": ads}