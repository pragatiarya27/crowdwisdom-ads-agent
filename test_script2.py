import json

with open('data/scripts_output.json', 'r') as f:
    scripts = json.load(f)

# Print first 1500 chars of script 2 (data_based)
print(scripts[1]['script'][:1500])
