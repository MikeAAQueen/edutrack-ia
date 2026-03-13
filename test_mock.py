import requests
import json
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:QXhhKOtR"
r = requests.get(f"{XANO_API_URL}/disciplinas", headers={"Authorization": "Bearer mock_jwt_token_123"})
print("mock token request status:", r.status_code)
print(r.text)
