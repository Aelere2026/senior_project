import requests

BASE = "https://api.elections.kalshi.com/trade-api/v2"

params = {
    "status": "open",   # only open markets
    "limit": 100
}

response = requests.get(f"{BASE}/markets", params=params)
data = response.json()

markets = data.get("markets", [])

for market in markets[:5]:
    print(market.get("title"))
