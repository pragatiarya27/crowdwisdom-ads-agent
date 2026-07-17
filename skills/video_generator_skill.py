import json
import os
import re
import subprocess
from hermes.skill import BaseSkill
from config import OUTPUT_DIR

import os as _os
env = _os.environ.copy()
env["PATH"] = r"C:\ffmpeg\bin;" + env.get("PATH", "")

class VideoGeneratorSkill(BaseSkill):
    name = "video_generator_skill"

    def clean_text(self, text: str) -> str:
        text = text.encode("ascii", "ignore").decode("ascii")
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+', '', text)
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'VO:|Voiceover:|Visual:', '', text)
        text = re.sub(r'-{2,}', '', text)
        text = re.sub(r'\|.*', '', text)
        text = ' '.join(text.split())
        return text.strip()
    def truncate_clean_simple(self, text: str, max_chars: int = 280) -> str:
        """Split at last space, add ..."""
        if len(text) <= max_chars:
            return text
        
        cut = text[:max_chars]
        last_space = cut.rfind(" ")
        
        if last_space > 0:
            return cut[:last_space] + "..."
        return cut + "..."

    def parse_script(self, script_text: str) -> list:
        scenes = []
        sections = ["HOOK", "PROBLEM", "SOLUTION", "CTA",
                    "DATA", "INSIGHT", "CONCEPT", "PROOF"]
          # ✅ NEW: Handle **SECTION (X seconds):** format
        if "**HOOK" in script_text or "**DATA" in script_text:
            section_pattern = r'\*\*([A-Z]+)\s*\([^)]*\):\*\*\s*(.*?)(?=\*\*[A-Z]|\Z)'
            matches = re.findall(section_pattern, script_text, re.DOTALL)
            
            for title, content in matches:
                clean = self.clean_text(content.strip())
                if clean and len(clean) > 10:
                    scenes.append({
                        "title": title,
                        "text": self.truncate_clean_simple(clean, max_chars=400)
                    })
            return scenes[:4]

        # handle table format
        if "|" in script_text and "---" in script_text:
            rows = [line for line in script_text.split("\n")
                    if "|" in line and "---" not in line
                    and "Time" not in line and "Section" not in line]
            section_names = ["HOOK", "DATA", "INSIGHT", "CTA"]
            for idx, row in enumerate(rows[:4]):
                cols = [c.strip() for c in row.split("|") if c.strip()]
                if len(cols) >= 2:
                    content = cols[-1].replace("*", "").strip()
                    clean = self.clean_text(content)
                    if clean and len(clean) > 10:
                        scenes.append({
                            "title": section_names[idx] if idx < len(section_names) else f"SCENE {idx+1}",
                            "text": self.truncate_clean_simple(clean, max_chars=400)  # ✅ Use truncate method
                        })
            return scenes[:4]

        current_section = None
        current_text = ""

        for line in script_text.split("\n"):
            line = line.strip()
            if not line:
                continue

            # check if line contains a section keyword
            found_section = None
            for section in sections:
                if section in line.upper():
                    # extract everything after the section name
                    idx = line.upper().find(section)
                    after = line[idx + len(section):].strip()
                    after = re.sub(r'^[\s:*\(\)0-9a-z\-seconds]+', '', after).strip()
                    after = after.lstrip('.')
                    
                    if current_section and current_text.strip():
                        clean = self.clean_text(current_text)
                        if len(clean) > 10:
                            scenes.append({
                                "title": current_section,
                                "text": self.truncate_clean_simple(clean, max_chars=400)
                            })
                    current_section = section
                    current_text = after + " " if after else ""
                    found_section = section
                    break

            if not found_section and current_section:
                current_text += line + " "

        # add last section
        if current_section and current_text.strip():
            clean = self.clean_text(current_text)
            if len(clean) > 10:
                scenes.append({
                    "title": current_section,
                    "text": self.truncate_clean_simple(clean, max_chars=300)
                })

        return scenes[:4]
    # COMPLETE OPTIMIZED generate_html() METHOD
# Copy and replace your existing generate_html() method with this

    def generate_html(self, scenes: list, script_type: str) -> str:
        scene_duration = 8 
        total_duration = len(scenes) * scene_duration

        scenes_html = ""
        for i, scene in enumerate(scenes):
            start_time = i * scene_duration
            title = scene["title"]
            
            # Text is already truncated properly in parse_script()
            text = scene["text"].replace('"', "'").replace('\n', ' ').strip()

            scenes_html += f"""
        <div class="clip" data-start="{start_time}" data-duration="{scene_duration}"
            style="position:absolute;left:0;top:0;
                    width:854px;height:480px;
                    background:linear-gradient(135deg,#0f2041,#193764);
                    display:flex;flex-direction:column;
                    align-items:center;justify-content:center;
                    box-sizing:border-box;padding:40px 60px;
                    text-align:center;">
            <div style="color:#FFD700;font-size:36px;font-weight:800;
                        text-transform:uppercase;letter-spacing:3px;
                        margin-bottom:20px;text-align:center;
                        width:734px;word-wrap:break-word;">
            {title}
            </div>
            <div style="color:#FFFFFF;font-size:16px;line-height:1.5;
                        text-align:center;width:734px;font-weight:400;
                        word-wrap:break-word;overflow-wrap:break-word;
                        white-space:normal;max-height:300px;overflow:hidden;">
            {text}
            </div>
            <div style="position:absolute;bottom:30px;left:0;right:0;
                        text-align:center;color:#87CEEB;
                        font-size:14px;letter-spacing:1px;">
            CrowdWisdomTrading.com
            </div>
        </div>
        """

        html = f"""<!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <meta name="hf-width" content="854">
        <meta name="hf-height" content="480">
        <meta name="hf-duration" content="{total_duration}">
        <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ width: 854px; height: 480px; overflow: hidden;
                font-family: 'Inter', 'Arial', sans-serif;
                background: #0f2041; }}
        </style>
        </head>
        <body>
        <div data-composition-id="main"
            data-width="854"
            data-height="480"
            data-duration="{total_duration}"
            data-start="0"
            style="position:relative;width:854px;height:480px;overflow:hidden;">
        {scenes_html}
        </div>
        <script>
        window.__timelines = window.__timelines || {{}};
        window.__timelines["main"] = gsap.timeline()
            .to({{}}, {{duration: {total_duration}}});
        </script>
        </body>
        </html>"""
        return html

    def render_video(self, html_content: str, script_type: str, index: int) -> str:
        project_name = f"ad_{script_type}_{index}"
        project_dir = os.path.join(OUTPUT_DIR, project_name)
        os.makedirs(project_dir, exist_ok=True)

        html_path = os.path.join(project_dir, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"📄 [VIDEO] HTML written: {html_path}")
        print(f"🎬 [VIDEO] Rendering with HyperFrames...")

        result = subprocess.run(
            ["cmd", "/c", "npx", "hyperframes", "render"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=1200,
            env=env
        )

        if result.returncode != 0:
            print(f"⚠️ [VIDEO] HyperFrames stderr: {result.stderr[-500:]}")
            raise Exception(f"HyperFrames render failed: {result.stderr[-200:]}")

        renders_dir = os.path.join(project_dir, "renders")
        if os.path.exists(renders_dir):
            mp4_files = [f for f in os.listdir(renders_dir) if f.endswith(".mp4")]
            if mp4_files:
                video_path = os.path.join(renders_dir, mp4_files[0])
                print(f"✅ [VIDEO] Video saved: {video_path}")
                return video_path

        raise Exception("No MP4 file found in renders folder")

    def run(self, input: dict) -> dict:
        scripts = input.get("scripts", [])
        if not scripts:
            with open("data/scripts_output.json", "r", encoding="utf-8") as f:
                scripts = json.load(f)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        video_paths = []

        for i, script in enumerate(scripts):
            script_type = script.get("type", f"script_{i}")
            script_text = script.get("script", "")

            if not script_text or script_text == "None":
                print(f"⚠️ Skipping empty script {i+1}")
                continue

            print(f"\n🎬 [VIDEO] Processing script {i+1}: {script_type}")
            scenes = self.parse_script(script_text)

            if not scenes:
                print(f"⚠️ No scenes found for script {i+1}")
                continue

            print(f"📝 [VIDEO] Found {len(scenes)} scenes")
            html = self.generate_html(scenes, script_type)
            video_path = self.render_video(html, script_type, i+1)
            video_paths.append(video_path)

        return {"video_paths": video_paths, "count": len(video_paths)}