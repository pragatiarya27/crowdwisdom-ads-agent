import json
import sys
from skills.video_generator_skill import VideoGeneratorSkill

print('[START] Loading scripts...')
sys.stdout.flush()

with open('data/scripts_output.json', 'r') as f:
    scripts = json.load(f)

print(f'[LOADED] Found {len(scripts)} scripts')
sys.stdout.flush()

skill = VideoGeneratorSkill()
for i, script in enumerate(scripts):
    print(f'[VIDEO {i+1}] Rendering {script.get("type", "unknown")}...')
    sys.stdout.flush()
    
    scenes = skill.parse_script(script['script'])
    print(f'[SCENES] Found {len(scenes)} scenes')
    sys.stdout.flush()
    
    html = skill.generate_html(scenes, script['type'])
    print(f'[HTML] Generated composition')
    sys.stdout.flush()
    
    video_path = skill.render_video(html, script['type'], i+1)
    print(f'[COMPLETE] Video saved: {video_path}')
    sys.stdout.flush()

print('[DONE] All videos rendered!')
