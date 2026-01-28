"""Verify the updated workflow"""
import json

wf = json.load(open('backup_workflows/Caption_Flow_V2_oRYSQ9tk63yPJaqt_UPDATED.json', encoding='utf-8-sig'))

webhook = next((n for n in wf['nodes'] if n['name'] == 'CaptionFlow Webhook'), None)
respond = next((n for n in wf['nodes'] if n['name'] == 'Respond to Frontend'), None)

print("=" * 60)
print("WORKFLOW VERIFICATION")
print("=" * 60)

print("\n=== CaptionFlow Webhook Node ===")
if webhook:
    print(f"  responseMode: {webhook['parameters'].get('responseMode', 'NOT SET')}")
else:
    print("  NOT FOUND!")

print("\n=== Respond to Frontend Node ===")
if respond:
    print(f"  ID: {respond.get('id')}")
    print(f"  Type: {respond.get('type')}")
    print(f"  Position: {respond.get('position')}")
    params = respond.get('parameters', {})
    print(f"  respondWith: {params.get('respondWith')}")
    print(f"  responseBody: {params.get('responseBody', 'N/A')[:200]}...")
else:
    print("  NOT FOUND!")

print("\n=== Connections for 'Upload Image to Cloudinary' ===")
conn = wf.get('connections', {}).get('Upload Image to Cloudinary', {})
print(json.dumps(conn, indent=2))

print("\n=== Connections for 'Respond to Frontend' ===")
conn2 = wf.get('connections', {}).get('Respond to Frontend', {})
print(json.dumps(conn2, indent=2))
