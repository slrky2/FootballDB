import requests, json, os, re

url = "https://www.espn.com/nfl/boxscore/_/gameId/401872995"
html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

marker = re.compile(r"window\['__espnfitt__'\]\s*=\s*")

def load_game_from_html(html):
    m = marker.search(html)
    data, _ = json.JSONDecoder().raw_decode(html[m.end():])
    return data["page"]["content"]["gamepackage"]

# only grab the important data from the scrape
item = load_game_from_html(html)
with open("game_data.json", "w") as f:
    json.dump(item, f)

with open("game_data.json", encoding="utf-8") as f:
    data = json.load(f)
    print("GAME_ID: " + data["gmStrp"]["gid"])
    print('date' + data["gmSwtchrMta"]["firstPillOverride"]["date"])
    print(data["prsdTms"]["home"]["displayName"] + " VS " + data["prsdTms"]["away"]["displayName"])