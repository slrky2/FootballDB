import requests, json, os

url = "https://www.espn.com/nfl/player/_/id/4426515/puka-nacua"
html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

marker = "window['__espnfitt__']="
start = html.index(marker) + len(marker)
data, _ = json.JSONDecoder().raw_decode(html[start:])
player = data["page"]["content"]["player"]

games = {}  # keyed by game id

print ('Name:' + player["plyrHdr"]["ath"]["dspNm"] + '\nPosition:'+ player["plyrHdr"]["ath"]["posAbv"] + '\nTeam:' + player["plyrHdr"]["ath"]["tm"])


for table in player["gmlg"]["stats"]: # for each game in his table, in which he has stats (not zeros)
    category = table["title"].lower()          # receiving / rushing / fumbles
    labels = [h["ttl"] for h in table["headings"]]   # full names avoid the duplicate YDS/AVG/TD labels

    for row in table["rows"]:
        g = games.setdefault(row["id"], {
            "game_id": row["id"],
            "date": row["dt"],
            "opponent": row["opp"]["abbr"],
            "home": row["opp"]["atVs"] == "vs",
            "result": row["res"]["abbr"],
            "score": row["res"]["score"],
        })
        for label, value in zip(labels, row["stats"]):
            g[f"{category}_{label}"] = float(value)

for g in games.values():
    print(g)