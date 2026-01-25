
import requests

URL = "https://emanueleserra.app.n8n.cloud/webhook/ai-proxy"

def test():
    print(f"Testing URL: {URL}")
    
    # 1. Test OPTIONS (Preflight)
    print("\n1. Testing OPTIONS request...")
    try:
        res = requests.options(URL, headers={
            "Origin": "https://bloom-2-0.vercel.app",
            "Access-Control-Request-Method": "POST"
        })
        print(f"   Status: {res.status_code}")
        print(f"   Headers: {res.headers}")
    except Exception as e:
        print(f"   Failed: {e}")

    # 2. Test POST (Direct)
    print("\n2. Testing POST request...")
    try:
        res = requests.post(URL, json={"model": "test"}, headers={
            "Content-Type": "application/json"
        })
        print(f"   Status: {res.status_code}")
        print(f"   Response: {res.text[:200]}")
    except Exception as e:
        print(f"   Failed: {e}")

if __name__ == "__main__":
    test()
