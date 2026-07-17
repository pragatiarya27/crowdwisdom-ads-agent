import json
from skills.video_generator_skill import VideoGeneratorSkill

with open('data/scripts_output.json', 'r') as f:
    scripts = json.load(f)

skill = VideoGeneratorSkill()
scenes = skill.parse_script(scripts[1]['script'])  # ← Change to [1] for data_based

for i, scene in enumerate(scenes):
    print(f'Scene {i+1}: {scene["title"]}')
    print(f'Text: {scene["text"][:100]}...')  # First 100 chars
    print('---')