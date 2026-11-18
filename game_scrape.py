import requests, json, os, re, sqlite3, game_scrape

game_url = "https://www.espn.com/nfl/boxscore/_/gameId/401872995"
html = requests.get(game_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

marker = re.compile(r"window\['__espnfitt__'\]\s*=\s*")

connection = sqlite3.connect("football.db")
cursor = connection.cursor()

cursor.execute("""""
    CREATE TABLE IF NOT EXISTS players
    id = INTEGER PRIMARY KEY,
    name = TEXT
    position TEXT,
    team TEXT,
    age INTEGER, 
            """)

def getPlayerInfo(url):
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
    marker = "window['__espnfitt__']="
    start = html.index(marker) + len(marker)
    data, _ = json.JSONDecoder().raw_decode(html[start:])
    player = data["page"]["content"]["player"]

    cursor.execute(
        "INSERT INTO players (position, team, age) VALUES (?, ?, ?)"
        (player["plyrHdr"]["ath"]["posAbv"], player["plyrHdr"]["ath"]["tm"]), 
    )
    print ('\nPosition:'+ player["plyrHdr"]["ath"]["pos"] + '\nAbrev:' + player["plyrHdr"]["ath"]["posAbv"]+ '\nTeam:' + player["plyrHdr"]["ath"]["tm"])


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
    print('date ' + data["gmSwtchrMta"]["firstPillOverride"]["date"])
    print(data["prsdTms"]["home"]["displayName"] + " VS " + data["prsdTms"]["away"]["displayName"])

    # print all stats for quarterbacks (eventually add database code)
    # print(data["bxscr"][0]["stats"][0]["athlts"][0]["athlt"]["dspNm"])
    # prints out sam darnold.

    connection = sqlite3.connect("football.db")
    cursor = connection.cursor()

    for team in data["bxscr"]:
        print('\n\n', team["tm"]["dspNm"], '\n\n')
        for stat_catagories in team["stats"]:
            s = stat_catagories["keys"]
            for players in stat_catagories["athlts"]:
                p = players["stats"]
                statsheet = list(zip(s,p))
                print(players["athlt"]["dspNm"], end=':     ')
                player_id = (players["athlt"]["id"])
                player_url = f"https://www.espn.com/nfl/player/_/id/{player_id}"
                getPlayerInfo(player_url)
                print(statsheet)