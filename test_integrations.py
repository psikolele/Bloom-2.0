
import requests
import json
import time

# Conf
AUTH_URL = "https://emanueleserra.app.n8n.cloud/webhook/auth"
CAPTION_URL = "https://emanueleserra.app.n8n.cloud/webhook/caption-flow"
BRAND_URL = "https://emanueleserra.app.n8n.cloud/webhook/94f98082-9ced-4244-b493-3d54d7328478"

def test_endpoint(name, url, payload):
    print(f"\n🧪 Testing {name}...")
    print(f"   URL: {url}")
    try:
        start = time.time()
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        duration = time.time() - start
        
        print(f"   Status: {res.status_code}")
        print(f"   Time: {duration:.2f}s")
        print(f"   Response: {res.text[:200]}")
        
        if res.ok:
            print("   ✅ SUCCESS")
            return True
        else:
            print("   ❌ FAILURE")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    print("🚀 Running Mock Data Integration Tests on All Active Workflows...")
    
    # 1. Auth Login
    test_endpoint("Auth (Login)", AUTH_URL, {
        "mode": "login",
        "username": "test_user_bloom_v2",
        "password": "Password123!"
    })
    
    # 2. Auth Register
    test_endpoint("Auth (Register)", AUTH_URL, {
        "mode": "register",
        "username": "new_user_bloom_v2",
        "email": "test@example.com",
        "password": "Password123!"
    })

    # 3. Caption Flow
    test_endpoint("Caption Flow", CAPTION_URL, {
        "nome_azienda": "Bloom Test Corp",
        "sito_web": "https://bloom-test.com",
        "indirizzo": "Via Roma 1",
        "email_contatto": "info@bloom-test.com",
        "strategia_aziendale": "Dominare il mercato AI",
        "tipologia_comunicazione": "Istituzionale",
        "social_platforms": ["LinkedIn", "Twitter/X"],
        "prodotti": [{"nome": "BloomAI", "descrizione": "AI Agent"}],
        "immagini": []
    })
    
    # 4. Brand Profile
    test_endpoint("Brand Profile", BRAND_URL, {
        "website": "https://example.com",
        "brand_name": "Example Brand",
        "settore": "Tech",
        "tone_voice": "Professional",
        "target_age": "25-45",
        "target_geo": "Italy",
        "keywords": ["tech", "ai", "future"],
        "competitor_1_name": "Competitor A"
    })

if __name__ == "__main__":
    main()
