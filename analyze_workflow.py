"""Analyze workflow to understand when response is sent"""
import json

wf = json.load(open('backup_workflows/Caption_Flow_V2_LATEST.json', encoding='utf-8-sig'))

print("=" * 70)
print("WORKFLOW ANALYSIS - When does the webhook respond?")
print("=" * 70)

# Find the webhook node
webhook = next((n for n in wf['nodes'] if n['name'] == 'CaptionFlow Webhook'), None)
print(f"\n1. CaptionFlow Webhook:")
print(f"   responseMode: {webhook['parameters'].get('responseMode', 'NOT SET')}")

# Find Respond to Frontend
respond = next((n for n in wf['nodes'] if n['name'] == 'Respond to Frontend'), None)
if respond:
    print(f"\n2. Respond to Frontend Node:")
    print(f"   ID: {respond['id']}")
    print(f"   Position: {respond.get('position')}")
    
# Trace the path from Webhook to Respond to Frontend
print("\n3. Tracing path from Webhook to Respond:")

connections = wf.get('connections', {})

def find_path(start, end, connections, path=None):
    if path is None:
        path = [start]
    
    if start == end:
        return path
    
    if start not in connections:
        return None
    
    conn = connections[start]
    if 'main' in conn:
        for outputs in conn['main']:
            if outputs:
                for out in outputs:
                    next_node = out.get('node')
                    if next_node and next_node not in path:
                        new_path = path + [next_node]
                        result = find_path(next_node, end, connections, new_path)
                        if result:
                            return result
    return None

path = find_path('CaptionFlow Webhook', 'Respond to Frontend', connections)
if path:
    print(f"   Path: {' -> '.join(path)}")
else:
    print("   Could not trace direct path")

# Show all connections leading TO Respond to Frontend
print("\n4. What connects TO 'Respond to Frontend':")
for node_name, conn in connections.items():
    if 'main' in conn:
        for outputs in conn['main']:
            if outputs:
                for out in outputs:
                    if out.get('node') == 'Respond to Frontend':
                        print(f"   {node_name} -> Respond to Frontend")

# Show what Respond to Frontend connects to
print("\n5. 'Respond to Frontend' connects TO:")
if 'Respond to Frontend' in connections:
    for outputs in connections['Respond to Frontend']['main']:
        if outputs:
            for out in outputs:
                print(f"   -> {out.get('node')}")

# Check when the long operations happen (Image generation)
print("\n6. Key nodes in the workflow:")
key_nodes = ['4a. Create Image Task (Kie)', '4b. Wait for Generation', '4c. Get Image Result (Kie)', 'Upload Image to Cloudinary']
for kn in key_nodes:
    node = next((n for n in wf['nodes'] if n['name'] == kn), None)
    if node:
        print(f"   - {kn}")
        if '4b' in kn and 'parameters' in node:
            wait_time = node['parameters'].get('unit', 'unknown')
            wait_amount = node['parameters'].get('amount', 'unknown')
            print(f"     Wait: {wait_amount} {wait_time}")
