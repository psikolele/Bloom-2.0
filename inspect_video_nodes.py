import json

target_nodes = ["Video Prompt3", "Text to Video2", "Wait4", "Get Video4", "If4", "Video URL4"]

try:
    with open(r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows\Caption_Flow_V3_ANALYSIS.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    print(f"Workflow: {data.get('name')}")
    
    for node in data.get('nodes', []):
        if node.get('name') in target_nodes:
            print(f"\n--- NODE: {node.get('name')} ({node.get('type')}) ---")
            print(json.dumps(node, indent=2))

except Exception as e:
    print(f"Error: {e}")
