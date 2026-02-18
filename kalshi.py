import time
import requests

BASE = "https://api.elections.kalshi.com/trade-api/v2"

# 1) Pull open markets
params = {
    "status": "open",
    "limit": 100
}

response = requests.get(f"{BASE}/markets", params=params, timeout=30)
response.raise_for_status()
data = response.json()

markets = data.get("markets", [])

def get_top_of_book(ticker: str):
    """
    Returns (best_yes_bid, best_yes_ask) in cents if available.
    Kalshi orderbook returns bids only for YES and NO.
    YES ask can be inferred from NO bid: yes_ask = 100 - best_no_bid.
    """
    ob_resp = requests.get(f"{BASE}/markets/{ticker}/orderbook", timeout=30)
    ob_resp.raise_for_status()
    ob = ob_resp.json()["orderbook"]

    yes_bids = ob.get("yes", [])  # list like [[price, qty], ...]
    no_bids  = ob.get("no", [])

    best_yes_bid = yes_bids[0][0] if yes_bids else None
    best_no_bid  = no_bids[0][0]  if no_bids  else None

    best_yes_ask = (100 - best_no_bid) if best_no_bid is not None else None
    return best_yes_bid, best_yes_ask

# 2) Print first 5 markets with live-ish prices from the orderbook
for market in markets[:5]:
    ticker = market.get("ticker")
    title = market.get("title")

    if not ticker:
        continue

    try:
        yes_bid, yes_ask = get_top_of_book(ticker)

        # Optional mid if both sides available
        mid = None
        if yes_bid is not None and yes_ask is not None:
            mid = (yes_bid + yes_ask) / 2

        print(f"\n{title}")
        print(f"Ticker: {ticker}")
        print(f"YES bid: {yes_bid}¢ | YES ask: {yes_ask}¢ | Mid: {mid if mid is not None else 'N/A'}")

        # Be nice to the API if you scale this up
        time.sleep(0.15)

    except requests.HTTPError as e:
        print(f"\n{title}\nTicker: {ticker}\nError pulling orderbook: {e}")
