import requests, json, os, re, sqlite3

game_url = "https://www.espn.com/nfl/boxscore/_/gameId/401872995"
gameHtml = requests.get(game_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

marker = re.compile(r"window\['__espnfitt__'\]\s*=\s*")

connection = sqlite3.connect("football.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        name TEXT,
        position TEXT,
        team TEXT,
        age TEXT
    )
""")




def loadPlayerFromHtml(html):
    match = marker.search(html)
    if match is None:
        raise ValueError("ESPN data marker not found in player HTML")
    data, _ = json.JSONDecoder().raw_decode(html[match.end():])
    return data["page"]["content"]["player"]

    #         (player["plyrHdr"]["ath"]["posAbv"], player["plyrHdr"]["ath"]["tm"], player["plyrHdr"]["ath"]["dob"]  ) 

def loadGameFromHtml(html):
    match = marker.search(html)
    if match is None:
        raise ValueError("ESPN data marker not found in game HTML")
    data, _ = json.JSONDecoder().raw_decode(html[match.end():])
    return data["page"]["content"]["gamepackage"]

# only grab the GAME data from the scrape
item = loadGameFromHtml(gameHtml)
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

    numStats = 0

    for team in data["bxscr"]:
        print('\n\n', team["tm"]["dspNm"], '\n\n')
        for stat_catagories in team["stats"]:
            s = stat_catagories["keys"]
            
            numStats += 1
            print(s, ':  ', numStats)
            for players in stat_catagories["athlts"]:
                p = players["stats"]
                statsheet = list(zip(s,p))
                # print(players["athlt"]["dspNm"], end=':     ')
                player_id = (players["athlt"]["id"])
                name = players["athlt"]["dspNm"] 
                
                # playerUrl = f"https://www.espn.com/nfl/player/_/id/{player_id}"
                # playerHtml = requests.get(playerUrl, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
                
                # pItem = loadPlayerFromHtml(playerHtml)
                # with open(f"{name}_data.json", "w") as f:
                #     json.dump(pItem, f)
        
                # playerItem = loadPlayerFromHtml(playerHtml)
                # cursor.execute(
                #     "INSERT INTO players(id, name, position, team, age) VALUES (?, ?, ?, ?, ?)",
                #     (player_id, name, playerItem["plyrHdr"]["ath"]["posAbv"], playerItem["plyrHdr"]["ath"]["tm"], playerItem["plyrHdr"]["ath"]["dob"]),
                # )
                # print(statsheet)
                connection.commit()