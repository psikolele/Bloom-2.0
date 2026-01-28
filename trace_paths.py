"""Full connection analysis - output to file"""
import json

wf = json.load(open('backup_workflows/Caption_Flow_V2_LATEST.json', encoding='utf-8-sig'))
conn = wf['connections']

output = []

output.append("=" * 70)
output.append("WORKFLOW NODES")
output.append("=" * 70)

for node in wf['nodes']:
    if 'Sticky' not in node['name']:
        output.append(f"  - {node['name']}")

output.append("")
output.append("=" * 70)
output.append("ALL CONNECTIONS")
output.append("=" * 70)

for node_name, connections in conn.items():
    main = connections.get('main', [])
    if main:
        for i, outputs in enumerate(main):
            if outputs:
                for out in outputs:
                    target = out.get('node', 'UNKNOWN')
                    output.append(f"{node_name} -> {target}")

output.append("")
output.append("=" * 70)
output.append("PATH FROM WEBHOOK TO RESPOND")
output.append("=" * 70)

# Manual trace
current = 'CaptionFlow Webhook'
path = [current]
visited = set([current])

def get_next_nodes(node_name, connections):
    if node_name not in connections:
        return []
    main = connections[node_name].get('main', [])
    next_nodes = []
    for outputs in main:
        if outputs:
            for out in outputs:
                next_nodes.append(out.get('node'))
    return next_nodes

# BFS to find path to Respond to Frontend
from collections import deque
queue = deque([(current, [current])])
found_path = None

while queue:
    node, path = queue.popleft()
    if node == 'Respond to Frontend':
        found_path = path
        break
    for next_node in get_next_nodes(node, conn):
        if next_node not in visited:
            visited.add(next_node)
            queue.append((next_node, path + [next_node]))

if found_path:
    output.append("Path found:")
    for i, node in enumerate(found_path):
        output.append(f"  {i+1}. {node}")
else:
    output.append("No path found to Respond to Frontend!")

# Also check for "Risposta Successo" node which might be responding
output.append("")
output.append("=" * 70)
output.append("CHECK FOR OTHER RESPOND NODES")
output.append("=" * 70)

for node in wf['nodes']:
    if 'respond' in node['name'].lower() or 'risposta' in node['name'].lower():
        output.append(f"\nNode: {node['name']}")
        output.append(f"  Type: {node.get('type')}")
        if 'parameters' in node:
            output.append(f"  Parameters: {json.dumps(node['parameters'], indent=4)[:500]}")

# Check CaptionFlow Webhook settings
output.append("")
output.append("=" * 70)
output.append("WEBHOOK NODE SETTINGS")
output.append("=" * 70)
webhook = next((n for n in wf['nodes'] if n['name'] == 'CaptionFlow Webhook'), None)
if webhook:
    output.append(json.dumps(webhook, indent=2))

# Write to file
with open('workflow_analysis.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Analysis written to workflow_analysis.txt")
