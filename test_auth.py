import requests
XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:QXhhKOtR"
print("Testing GET without any token:")
resp = requests.get(f"{XANO_API_URL}/disciplinas")
print(resp.status_code, resp.text)
