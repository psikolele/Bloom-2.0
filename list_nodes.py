import json

try:
    with open(r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows\Caption_Flow_V3_ANALYSIS.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    print(f"Workflow Name: {data.get('name')}")
    print(f"Updated At: {data.get('updatedAt')}")
    
    print("\nNodes:")
    for node in data.get('nodes', []):
        print(f" - [{node.get('type')}] {node.get('name')} (ID: {node.get('id')})")
        # Check if it has 'video' in parameters
        params = str(node.get('parameters', {}))
        if 'video' in params.lower():
            print(f"   *** CONTAINS 'VIDEO' IN PARAMETERS ***")
            
except Exception as e:
    print(f"Error: {e}")
