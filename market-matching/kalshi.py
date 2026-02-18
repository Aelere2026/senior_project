import requests

BASE = "https://api.elections.kalshi.com/trade-api/v2"

# Pull open markets
params = {
    "status": "open",
    "limit": 100
}

response = requests.get(f"{BASE}/markets", params=params, timeout=30)
response.raise_for_status()
data = response.json()

markets = data.get("markets", [])

# Print first 5 markets with matching-relevant info
for market in markets[:5]:
    print("\n---")
    print("Title:", market.get("title"))
    print("Ticker:", market.get("ticker"))
    print("Event Ticker:", market.get("event_ticker"))
    print("Series Ticker:", market.get("series_ticker"))
    print("Close Time:", market.get("close_time"))
    print("Category:", market.get("category"))
    print("Rules:", market.get("rules_primary"))
