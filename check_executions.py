"""Check execution details"""
import requests
import json

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMmRmNzQ5NC1hNjVjLTRjOTAtOTE5MC00NmViOWI4ODg5OGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY4NTEyOTE5fQ.T-W7tlxC7dAA0dPHusS7yuZLpX-qAzuzYCUT653cC0k"
BASE_URL = "https://emanueleserra.app.n8n.cloud/api/v1"

# Get the last execution
resp = requests.get(
    f"{BASE_URL}/executions?workflowId=oRYSQ9tk63yPJaqt&limit=3",
    headers={"X-N8N-API-KEY": API_KEY}
)
executions = resp.json()['data']

print("=" * 70)
print("RECENT EXECUTIONS")
print("=" * 70)

for ex in executions:
    print(f"\nExecution ID: {ex['id']}")
    print(f"  Status: {ex['status']}")
    print(f"  Started: {ex.get('startedAt', 'N/A')}")
    print(f"  Stopped: {ex.get('stoppedAt', 'N/A')}")
    print(f"  Finished: {ex.get('finished', 'N/A')}")
    
# Get detailed info on the most recent one
print("\n" + "=" * 70)
print(f"DETAILED EXECUTION: {executions[0]['id']}")
print("=" * 70)

resp2 = requests.get(
    f"{BASE_URL}/executions/{executions[0]['id']}",
    headers={"X-N8N-API-KEY": API_KEY}
)
exec_detail = resp2.json()

# Check what nodes ran
if 'data' in exec_detail and exec_detail['data']:
    run_data = exec_detail.get('data', {}).get('resultData', {}).get('runData', {})
    if run_data:
        print("\nNodes executed:")
        for node_name in run_data.keys():
            print(f"  - {node_name}")
    else:
        print("\nNo runData available (execution may not have full data)")
else:
    print("\nExecution data structure:")
    print(json.dumps(exec_detail, indent=2, default=str)[:2000])
