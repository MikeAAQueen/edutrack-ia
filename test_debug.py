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

# Create User 1
u1_email = f"u1_{uuid.uuid4().hex[:6]}@example.com"
r = req_with(f"{AUTH_API_URL}/auth/signup", "POST", {"name": "User 1", "email": u1_email, "password": "123"})
t1 = r.json().get("authToken")

# Create User 2
u2_email = f"u2_{uuid.uuid4().hex[:6]}@example.com"
r = req_with(f"{AUTH_API_URL}/auth/signup", "POST", {"name": "User 2", "email": u2_email, "password": "123"})
t2 = r.json().get("authToken")

print("User 1 fetching disciplines...")
p1 = req_with(f"{XANO_API_URL}/disciplinas", "GET", token=t1).json()
print("t1 count:", len(p1))

print("User 2 fetching disciplines...")
p2 = req_with(f"{XANO_API_URL}/disciplinas", "GET", token=t2).json()
print("t2 count:", len(p2))

# Post with User 1
print("User 1 creating discipline...")
r = req_with(f"{XANO_API_URL}/disciplinas", "POST", {"nome": f"Disc U1", "professor": "P1", "creditos": 2}, token=t1)
print("Create resp:", r.status_code, r.text)

print("User 2 fetching again...")
p2_after = req_with(f"{XANO_API_URL}/disciplinas", "GET", token=t2).json()
print("t2 count after u1 create:", len(p2_after))
if len(p2_after) > 0:
    print("User 2 sees:", json.dumps(p2_after, indent=2))
