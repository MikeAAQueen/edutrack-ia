import requests
import json
import uuid

AUTH_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:mibNtLvt"
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:QXhhKOtR"

def register_random_user():
    uid = str(uuid.uuid4())[:8]
    email = f"user_{uid}@example.com"
    url = f"{AUTH_API_URL}/auth/signup"
    payload = {"name": f"User {uid}", "email": email, "password": "password123"}
    resp = requests.post(url, json=payload)
    if resp.status_code in (200, 201):
        return resp.json().get("authToken"), email
    return None, None

def create_subject(token, name):
    url = f"{XANO_API_URL}/disciplinas"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"nome": name, "professor": "Prof Test", "creditos": 5}
    resp = requests.post(url, json=payload, headers=headers)
    return resp.status_code, resp.json()

def fetch_subjects(token, label):
    print(f"\nFetching subjects for {label}...")
    url = f"{XANO_API_URL}/disciplinas"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    try:
        data = resp.json()
        print(f"Status: {resp.status_code}. Count: {len(data)}")
        for idx, item in enumerate(data):
            print(f"  {idx+1}. {item.get('nome')} (user_id: {item.get('user_id')})")
    except:
        print("Response text:", resp.text)

if __name__ == "__main__":
    print("--- Testing Xano User Isolation ---")
    
    token_A, email_A = register_random_user()
    print(f"Registered User A: {email_A}")
    
    token_B, email_B = register_random_user()
    print(f"Registered User B: {email_B}")
    
    status, data = create_subject(token_A, "Subject for User A")
    print(f"User A created subject: {status}")
    
    fetch_subjects(token_A, "User A")
    fetch_subjects(token_B, "User B")
