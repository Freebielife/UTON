"""Discover indexed trading pools by jetton master without changing the trade feed."""
from decimal import Decimal
from urllib.parse import urlencode

from assets import MASTER, fetch
from badges import raw_friendly

API = "https://api.geckoterminal.com/api/v2"
REVIEWED_NON_NATIVE = "EQDW4TVALq3cOFA2F9y-LtXrzA4lNqEcXALFPyZ6ePKQuyXD"
NATIVE = "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c"


def collect(now, master=MASTER):
    token = raw_friendly(master)
    rows = {}
    for page in range(1, 11):
        query = urlencode({"include": "base_token,quote_token,dex", "page": page})
        result = fetch(f"/networks/ton/tokens/{master}/pools?{query}", api=API)
        included = {item["id"]: item["attributes"] for item in result.get("included", [])}
        for entry in result["data"]:
            attributes, relations = entry["attributes"], entry["relationships"]
            bases = [relations[k]["data"]["id"] for k in ("base_token", "quote_token")]
            tokens = [id_.removeprefix("ton_") for id_ in bases]
            sides = [raw_friendly(address) for address in tokens]
            if sides.count(token) != 1:
                raise ValueError("Unexpected assets in pool")
            other = 1 - sides.index(token)
            address = attributes["address"]
            # This GeckoTerminal entry labels a non-native pair as TON/uTON.
            # Confirm the actual assets with the DEX before displaying its quote.
            verified_symbol = None
            if raw_friendly(address) == raw_friendly(REVIEWED_NON_NATIVE):
                proof = fetch("/pools/" + address, api="https://api.ston.fi/v1")["pool"]
                actual = [proof["token0_address"], proof["token1_address"]]
                if [raw_friendly(t) for t in actual].count(token) != 1:
                    raise ValueError("STON.fi pool asset mismatch")
                tokens[other] = next(t for t in actual if raw_friendly(t) != token)
                verified_symbol = fetch("/jettons/" + tokens[other])["metadata"]["symbol"]
            dex = relations["dex"]["data"]["id"]
            reserve = attributes.get("reserve_in_usd")
            if reserve is not None and (not Decimal(reserve).is_finite() or Decimal(reserve) < 0):
                raise ValueError("Invalid liquidity")
            rows[raw_friendly(address)] = {
                "address": address,
                "token": tokens[other],
                "symbol": verified_symbol or ("TON" if tokens[other] == NATIVE else included[bases[other]]["symbol"]),
                "dex": included.get(dex, {}).get("name", dex),
                "liquidityUsd": reserve,
            }
        if len(result["data"]) < 20:
            return {"asOf": now, "rows": list(rows.values())}
    raise RuntimeError("Pool pagination limit reached")
