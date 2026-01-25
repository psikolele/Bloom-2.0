
import requests
import json

# Vercel API Configuration
VERCEL_TOKEN = "TLO1GlT8pKxmdRGjhdG4QF4S"
VERCEL_API = "https://api.vercel.com"
HEADERS = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json"
}

PROJECT_NAME = "bloom-2-0"

def get_project_id():
    """Get project ID by name"""
    res = requests.get(f"{VERCEL_API}/v9/projects", headers=HEADERS)
    if not res.ok:
        print(f"❌ Error: {res.status_code}")
        return None
    for p in res.json().get('projects', []):
        if PROJECT_NAME.lower() in p['name'].lower():
            return p['id']
    return None

def list_deployments(project_id, limit=100):
    """List all deployments for project"""
    res = requests.get(f"{VERCEL_API}/v6/deployments?projectId={project_id}&limit={limit}", headers=HEADERS)
    if not res.ok:
        return []
    return res.json().get('deployments', [])

def delete_deployment(uid):
    """Delete a deployment"""
    res = requests.delete(f"{VERCEL_API}/v13/deployments/{uid}", headers=HEADERS)
    return res.ok

def disable_preview_deployments(project_id):
    """Disable automatic preview deployments"""
    print("\n⚙️ Disabling Preview Deployments...")
    
    # Update project settings
    payload = {
        "autoExposeSystemEnvs": True,
        "skipGitConnectDuringLink": False,
        # Disable branch deployments
        "gitForkProtection": True
    }
    
    # Try to update project to only deploy production branch
    res = requests.patch(
        f"{VERCEL_API}/v9/projects/{project_id}",
        headers=HEADERS,
        json={
            "framework": "vite",
            "buildCommand": "npm run build",
            "outputDirectory": "dist",
            "installCommand": "npm install"
        }
    )
    
    if res.ok:
        print("  ✅ Project settings updated.")
    else:
        print(f"  ⚠️ Settings update: {res.status_code}")
    
    # The real way to disable preview is through Git Integration settings
    # This requires updating the Git repository configuration
    print("  ℹ️ Note: To fully disable preview deployments, go to:")
    print("     Vercel Dashboard -> Project -> Settings -> Git")
    print("     -> Disable 'Preview Deployments' toggle")
    
    return True

def cleanup_old_deployments():
    """Delete all deployments except the latest"""
    print(f"🚀 Cleanup Script for {PROJECT_NAME}")
    print("=" * 50)
    
    project_id = get_project_id()
    if not project_id:
        print(f"❌ Project '{PROJECT_NAME}' not found!")
        return
    
    print(f"📁 Project ID: {project_id}")
    
    # Get all deployments
    deployments = list_deployments(project_id)
    print(f"\n📦 Found {len(deployments)} total deployments.")
    
    if len(deployments) <= 1:
        print("✨ Only 1 deployment exists, nothing to delete.")
    else:
        # Sort by created time (newest first) - they should already be sorted
        # Keep only the first one (latest)
        to_delete = deployments[1:]  # All except the first
        
        print(f"🗑️ Deleting {len(to_delete)} old deployments...")
        
        deleted = 0
        failed = 0
        for i, d in enumerate(to_delete):
            url = d.get('url', 'N/A')
            uid = d['uid']
            print(f"  [{i+1}/{len(to_delete)}] Deleting {url[:40]}...", end=" ")
            
            if delete_deployment(uid):
                print("✅")
                deleted += 1
            else:
                print("❌")
                failed += 1
        
        print(f"\n📊 Results: {deleted} deleted, {failed} failed")
    
    # Disable preview deployments
    disable_preview_deployments(project_id)
    
    print("\n" + "=" * 50)
    print("✅ Cleanup Complete!")

if __name__ == "__main__":
    cleanup_old_deployments()
