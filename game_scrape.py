import requests, json, os, re

url = "https://www.espn.com/nfl/boxscore/_/gameId/401872995"
html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

marker = re.compile(r"window\['__espnfitt__'\]\s*=\s*")

def load_game_from_html(html):
    m = marker.search(html)
    data, _ = json.JSONDecoder().raw_decode(html[m.end():])
    return data["page"]["content"]["gamepackage"]

