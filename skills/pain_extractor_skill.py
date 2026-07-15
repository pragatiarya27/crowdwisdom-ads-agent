import json
import time
import requests
from hermes.skill import BaseSkill
from config import OPENROUTER_API_KEY, LLM_MODEL, LLM_BASE_URL, MAX_TOKENS

class PainExtractorSkill(BaseSkill):
    name = "pain_extractor_skill"

    def run(self, input: dict) -> dict:
        ads = input.get("ads", [])
        if not ads:
            with open("data/ads_results.json", "r") as f:
                ads = json.load(f)

        print(f"🧠 [EXTRACTOR] Analyzing {len(ads)} ads for pain points...")

        # combine ad texts for analysis
        ads_text = ""
        for i, ad in enumerate(ads[:10]):
            ads_text += f"\nAd {i+1}: {ad.get('body', '')} (Page: {ad.get('page_name', '')})\n"

        prompt = f"""
        Analyze these trading/investment ads and extract:
        1. Top 3 pain points traders face
        2. Top 3 emotional hooks used
        3. Top 3 unique selling points
        
        Ads:
        {ads_text}
        
        Respond in this exact JSON format:
        {{
            "pain_points": ["pain1", "pain2", "pain3"],
            "hooks": ["hook1", "hook2", "hook3"],
            "selling_points": ["sp1", "sp2", "sp3"]
        }}
        """

        # retry up to 3 times if rate limited
        resp_json = None
        for attempt in range(3):
            print(f"🔄 [EXTRACTOR] Attempt {attempt+1}/3...")
            response = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": LLM_MODEL,
                    "max_tokens": MAX_TOKENS,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            resp_json = response.json()
            if "choices" in resp_json:
                print("✅ [EXTRACTOR] LLM responded successfully!")
                break
            elif resp_json.get("error", {}).get("code") == 429:
                wait = resp_json["error"]["metadata"].get("retry_after_seconds", 30)
                print(f"⏳ [EXTRACTOR] Rate limited, waiting {wait} seconds...")
                time.sleep(wait + 2)
            else:
                raise Exception(str(resp_json))

        content = resp_json["choices"][0]["message"]["content"]

        # clean and parse JSON
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        concepts = json.loads(content)

        # save to file
        with open("data/pain_concepts.json", "w") as f:
            json.dump(concepts, f, indent=2)

        print(f"✅ [EXTRACTOR] Pain concepts extracted and saved!")
        print(f"   Pain points: {concepts['pain_points']}")
        return concepts