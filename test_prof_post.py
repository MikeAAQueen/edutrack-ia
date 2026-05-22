import requests
import json
import uuid

AUTH_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:mibNtLvt"
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:QXhhKOtR"

def req_with(url, method="GET", payload=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    if method == "POST":
        return requests.post(url, json=payload, headers=headers)
    else:
        return requests.get(url, headers=headers)

# Create User 
u1_email = f"prof_{uuid.uuid4().hex[:6]}@example.com"
r = req_with(f"{AUTH_API_URL}/auth/signup", "POST", {"name": "Prof User", "email": u1_email, "password": "123"})
t1 = r.json().get("authToken")

print("\nTesting /disciplinas POST")
r_post = req_with(f"{XANO_API_URL}/disciplinas", "POST", {"nome": "Disc Teste 1", "professores_id": 1, "creditos": 10}, token=t1)
print("Status:", r_post.status_code)
try:
    print("Data:", json.dumps(r_post.json(), indent=2))
except Exception:
    print("Text:", r_post.text)
