import requests
import urllib3
import time
import json
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://animalcompany.us-east1.nakamacloud.io/v2/account/session/refresh"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Basic NlVSdVRTbERLS2ZZYnVEVzo="
}

current_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIxYzllZjYxZS1hMGVkLTQzZDAtODY3Zi0wNGE1MWIxYzBiZTUiLCJ1aWQiOiJlYWViNDUzOS03MDUyLTQ0ZTEtOTNlYi1mYzJlMjFmYzA2M2MiLCJ1c24iOiJpWlBqX1R1d3UtdUI5bnFXIiwidnJzIjp7ImF1dGhJRCI6Ijk3ZTQyMzRiN2QxMjRjZWI5OGFiMWZlZDAxN2RjMGRkIiwiY2xpZW50VXNlckFnZW50IjoiU3RlYW1WUiAxLjc1LjIuMjk3OF85Zjg5YmY0OSIsImRldmljZUlEIjoiZGMxMThjYzA0M2M5ODZmOWY3YWNhZDkwOGYzOTUyNjJmODcyMWI5ZCJ9LCJleHAiOjE3ODAzNjI4NjMsImlhdCI6MTc4MDM0MTI2M30.JCLgK7_cWMa47ppMwaOTtfEVbhpd6yl3Et7EU4WDStU"

def do_refresh(token):
    resp = requests.post(URL, headers=HEADERS, json={"token": token}, verify=False)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Status: {resp.status_code}")
    
    data = resp.json()
    print(json.dumps(data, indent=2))

    try:
        chess_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inject.json")
        with open(chess_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to {chess_path}")
    except Exception as e:
        print(f"Warning: could not save inject.json: {e}")

    return data

while True:
    try:
        result = do_refresh(current_token)
        if result and "refresh_token" in result:
            current_token = result["refresh_token"]
            print("Token updated.")
        else:
            print("No refresh_token in response!")
    except Exception as e:
        print(f"Request failed: {e}")

    print("Sleeping 30 minutes...\n")
    time.sleep(30 * 60)