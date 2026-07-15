import json
import os
import re
from moviepy import TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from hermes.skill import BaseSkill
from config import OUTPUT_DIR

FONT = "C:/Windows/Fonts/arial.ttf"


class VideoGeneratorSkill(BaseSkill):
    name = "video_generator_skill"

    def clean_text(self, text: str) -> str:
        # removes all special characters and markdown
        text = text.encode("ascii", "ignore").decode("ascii")
        text = re.sub(r'<[^>]+>', '', text)        # remove HTML tags like <br>
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+', '', text)
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'VO:', '', text)
        text = re.sub(r'Voiceover:', '', text)
        text = re.sub(r'Visual:', '', text)
        text = re.sub(r'-{2,}', '', text)
        text = ' '.join(text.split())
        return text.strip()

    def truncate_clean(self, text: str, max_len: int) -> str:
        """Truncate text to max_len without cutting a word in half."""
        if len(text) <= max_len:
            return text
        cut = text[:max_len]
        last_space = cut.rfind(" ")
        if last_space > 0:
            cut = cut[:last_space]
        return cut.rstrip(",.;: ") + "..."

    def parse_script(self, script_text: str) -> list:
        scenes = []
        sections = ["HOOK", "PROBLEM", "SOLUTION", "CTA",
                    "DATA", "INSIGHT", "CONCEPT", "PROOF"]

        # handle table format (script 2 uses markdown table)
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
                            "text": self.truncate_clean(clean, 180)
                        })
            return scenes[:4]

        # normal format parsing
        lines = script_text.split("\n")
        current_section = None
        current_text = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            is_header = False
            for section in sections:
                if section in line.upper() and len(line) < 60:
                    if current_section and current_text.strip():
                        clean = self.clean_text(current_text)
                        if len(clean) > 20:
                            scenes.append({
                                "title": current_section,
                                "text": self.truncate_clean(clean, 180)
                            })
                    current_section = section
                    current_text = ""
                    is_header = True
                    break
            if not is_header and current_section:
                current_text += " " + line

        if current_section and current_text.strip():
            clean = self.clean_text(current_text)
            if len(clean) > 20:
                scenes.append({
                    "title": current_section,
                    "text": self.truncate_clean(clean, 180)
                })

        return scenes[:4]

    def create_video(self, scenes: list, script_type: str, index: int) -> str:
        print(f"Creating video for {script_type}...")
        colors = [
            (15, 32, 65),
            (25, 55, 100),
            (10, 45, 80),
            (5, 25, 55),
        ]
        VIDEO_W, VIDEO_H = 1280, 720
        SAFE_MARGIN = 120  # keep text away from left/right edges

        clips = []
        for i, scene in enumerate(scenes):
            duration = 8
            color = colors[i % len(colors)]

            bg = ColorClip(size=(VIDEO_W, VIDEO_H), color=color, duration=duration)

            # Title: fixed box + padding so ascenders/descenders don't get clipped
            title_clip = TextClip(
                text=scene["title"],
                font_size=45,
                color="yellow",
                font=FONT,
                method="caption",
                size=(VIDEO_W - SAFE_MARGIN, 100),
                margin=(None, 20),
                text_align="center",
                duration=duration
            ).with_position(("center", 60))

            # Body: auto-wraps within the box, never overflows frame width
            body_clip = TextClip(
                text=scene["text"],
                font_size=26,
                color="white",
                font=FONT,
                method="caption",
                size=(VIDEO_W - SAFE_MARGIN, VIDEO_H - 350),
                margin=(None, 15),
                text_align="center",
                duration=duration
            ).with_position(("center", 250))

            brand_clip = TextClip(
                text="CrowdWisdomTrading.com",
                font_size=20,
                color="white",
                font=FONT,
                duration=duration
            ).with_position(("center", VIDEO_H - 60))

            scene_clip = CompositeVideoClip([bg, title_clip, body_clip, brand_clip])
            clips.append(scene_clip)

        final_video = concatenate_videoclips(clips)
        video_filename = f"ad_{script_type}_{index}.mp4"
        video_path = os.path.join(OUTPUT_DIR, video_filename)
        final_video.write_videofile(
            video_path,
            fps=24,
            codec="libx264",
            audio=False,
            logger=None
        )
        print(f"Video saved: {video_path}")
        return video_path

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
                print(f"Skipping empty script {i+1}")
                continue

            print(f"\nProcessing script {i+1}: {script_type}")
            scenes = self.parse_script(script_text)

            if not scenes:
                print(f"No scenes found for script {i+1}")
                continue

            print(f"Found {len(scenes)} scenes")
            video_path = self.create_video(scenes, script_type, i+1)
            video_paths.append(video_path)

        return {"video_paths": video_paths, "count": len(video_paths)}