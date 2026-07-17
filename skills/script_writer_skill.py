import json
import time
import requests
from hermes.skill import BaseSkill
from config import OPENROUTER_API_KEY, LLM_BASE_URL, MAX_TOKENS

class ScriptWriterSkill(BaseSkill):
    name = "script_writer_skill"

    def call_llm(self, prompt: str) -> str:
        # calls LLM with retry logic
        for attempt in range(3):
            print(f"🔄 [SCRIPT] LLM attempt {attempt+1}/3...")
            response = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openrouter/free",
                    "max_tokens": MAX_TOKENS,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            resp = response.json()
            if "choices" in resp:
                return resp["choices"][0]["message"]["content"]
            elif resp.get("error", {}).get("code") == 429:
                wait = resp["error"]["metadata"].get("retry_after_seconds", 30)
                print(f"⏳ [SCRIPT] Rate limited, waiting {wait}s...")
                time.sleep(wait + 2)
            else:
                raise Exception(str(resp))
        raise Exception("LLM failed after 3 attempts")

    def write_pain_script(self, pain_points: list) -> dict:
        # script type 1 - based on pain points
        prompt = f"""
        Write a 30-second video ad script for CrowdWisdomTrading.com
        based on these trader pain points: {pain_points}
        
        Format:
        HOOK (3 seconds): [attention grabbing opening line]
        PROBLEM (10 seconds): [describe the pain]
        SOLUTION (12 seconds): [how CrowdWisdom solves it]
        CTA (5 seconds): [call to action]
        
       Make it emotional and relatable. Keep it short and punchy.
        IMPORTANT: Every section MUST end with a full stop (.).
        """
        content = self.call_llm(prompt)
        return {"type": "pain_based", "script": content}

    def write_data_script(self, rag_chunks: list) -> dict:
        # script type 2 - based on unique crowdwisdom data
        context = "\n".join(rag_chunks[:3])
        prompt = f"""
        Write a 30-second video ad script for CrowdWisdomTrading.com
        using this unique data and statistics: {context}
        
        Format:
        HOOK (3 seconds): [surprising stat or fact]
        DATA (10 seconds): [present the unique data]
        INSIGHT (12 seconds): [what this means for traders]
        CTA (5 seconds): [call to action]
        
        Make it data-driven and credible.
        IMPORTANT: Every section MUST end with a full stop (.).
        """
        content = self.call_llm(prompt)
        script_text = content if content and content.strip() != "None" else "Script generation pending - RAG data loaded successfully"
        return {"type": "data_based", "script": script_text}

    def write_crowd_wisdom_script(self, selling_points: list) -> dict:
        # script type 3 - how crowd wisdom helps trading
        prompt = f"""
        Write a 30-second video ad script for CrowdWisdomTrading.com
        explaining how crowd wisdom improves trading results.
        Key selling points: {selling_points}
        
        Format:
        HOOK (3 seconds): [what if you could know what thousands of traders think?]
        CONCEPT (10 seconds): [explain crowd wisdom in trading]
        PROOF (12 seconds): [how it helps, results]
        CTA (5 seconds): [visit CrowdWisdomTrading.com]
        
        Make it inspiring and trustworthy.
        IMPORTANT: Every section MUST end with a full stop (.).
       
        """
        content = self.call_llm(prompt)
        return {"type": "crowd_wisdom", "script": content}

    def run(self, input: dict) -> dict:
        pain_points = input.get("pain_points", [])
        selling_points = input.get("selling_points", [])
        rag_chunks = input.get("rag_chunks", [])

        print("✍️  [SCRIPT] Writing 3 ad scripts...")

        # generate all 3 script types
        script1 = self.write_pain_script(pain_points)
        print("✅ [SCRIPT] Pain-based script done!")

        script2 = self.write_data_script(rag_chunks)
        print("✅ [SCRIPT] Data-based script done!")

        script3 = self.write_crowd_wisdom_script(selling_points)
        print("✅ [SCRIPT] Crowd wisdom script done!")

        scripts = [script1, script2, script3]

        # save to file
        with open("data/scripts_output.json", "w") as f:
            json.dump(scripts, f, indent=2)

        print("✅ [SCRIPT] All scripts saved to data/scripts_output.json!")
        return {"scripts": scripts}