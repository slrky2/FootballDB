import requests, json, os, re, sqlite3
from pathlib import Path

game_url = "https://www.espn.com/nfl/boxscore/_/gameId/401872995"
# game_url = "https://www.espn.com/nfl/boxscore/_/gameId/401192711" # the 1980 game link.
gameHtml = requests.get(game_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
marker = re.compile(r"window\['__espnfitt__'\]\s*=\s*")

connection = sqlite3.connect("football.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
cursor.executescript(schema)

def seperateFraction(value):
    first, second = re.split(r"[/-]", value, maxsplit=1)
    return [int(first), int(second)]

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

    numStats = 0

    for team in data["bxscr"]:
        print('\n\n', team["tm"]["dspNm"], '\n\n')
        for stat_catagories in team["stats"]:
            s = stat_catagories["keys"]
            print(s[0])
            for players in stat_catagories["athlts"]:
                p = players["stats"]
                statsheet = list(zip(s,p))
                # print(players["athlt"]["dspNm"], end=':     ')
                playerID = players["athlt"]["id"]
                name = players["athlt"]["dspNm"] 
                
                playerUrl = f"https://www.espn.com/nfl/player/_/id/{playerID}"
                playerHtml = requests.get(playerUrl, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
                
                # pItem = loadPlayerFromHtml(playerHtml)
                # with open(f"{name}_data.json", "w") as f:
                #     json.dump(pItem, f)
        
                # TODO MAKE A DECISION, its probably smarter to download a players html once, instead of looking it up everytime over the course of the 17 games they can appear in a season
                playerItem = loadPlayerFromHtml(playerHtml)
                cursor.execute(
                    "INSERT INTO players(playerID, name, position, team, age) VALUES (?, ?, ?, ?, ?)"
                    "ON CONFLICT(playerID) DO NOTHING", # if the player was already loaded, leave it be.
                    (playerID, name, playerItem["plyrHdr"]["ath"]["posAbv"], playerItem["plyrHdr"]["ath"]["tm"], playerItem["plyrHdr"]["ath"]["dob"]),
                )
                
                match (s[0] if s else None):
                    case "completions/passingAttempts":
                        val = seperateFraction(p[0])
                        vals = seperateFraction(p[5])
                        cursor.execute(
                            "INSERT INTO passing(playerID, completions, pAttempts, pYards, YPPA, pTouchdowns, ints, sacks, YLtoSacks, adjQBR, QBR)"
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (playerID, val[0], val[1], p[1], p[2], p[3], p[4], vals[0], vals[1], p[6], p[7])
                        )
                        pass
                    case "rushingAttempts":
                        cursor.execute(
                            "INSERT INTO rushing(playerID, rAttempts, rYards, YPRA, rTouchdowns, longestRush)"
                            "VALUES(?, ?, ?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2], p[3], p[4])
                        )
                        pass
                    case "receptions":
                        cursor.execute(
                            "INSERT INTO receiving(playerID, receptions, receivingYards, yardsPerReception, receivingTouchdowns, longReception, receivingTargets)"
                            "VALUES(?, ?, ?, ?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5])
                        )
                        pass
                    case "fumbles":
                        cursor.execute(
                            "INSERT INTO fumbles(playerID, fumbles, fumblesLost, fumblesRecovered)"
                            "VALUES(?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2])
                        )
                        pass
                    case "totalTackles":
                        cursor.execute(
                            "INSERT INTO defense(playerID, totalTackles, soloTackles, sacks, tacklesForLoss, passesDefended, QBHits, DefensiveTouchdowns)"
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6])
                        )
                        pass
                    case "interceptions":
                        cursor.execute(
                            "INSERT INTO defensive_interceptions(playerID, interceptions, interceptionYards, interceptionTouchdowns)"
                            "VALUES(?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2])
                        )
                        pass
                    case "kickReturns":
                        cursor.execute(
                            "INSERT INTO kick_returns(playerID, kickReturns, kickReturnYards, yardsPerKickReturn, longKickReturn, kickReturnTouchdowns)"
                            "VALUES(?, ?, ?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2], p[3], p[4])
                        )
                        pass
                    case "puntReturns":
                        cursor.execute(
                            "INSERT INTO punt_returns(playerID, puntReturns, puntReturnYards, yardsPerPuntReturn, longPuntReturn, puntReturnTouchdowns)"
                            "VALUES(?, ?, ?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2], p[3], p[4])
                        )
                        pass
                    case "fieldGoalsMade/fieldGoalAttempts":
                        val = seperateFraction(p[0])
                        vals = seperateFraction(p[3])
                        cursor.execute(
                            "INSERT INTO kicking(playerID, fieldGoalsMade, fieldGoalAttempts, fieldgoalPct, longFieldGoalMade, extraPointsMade, extraPointAttempts, totalKickingPoints)"
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (playerID, val[0], val[1], p[1], p[2], vals[0], vals[1], p[4])
                        )
                        pass
                    case "punts":
                        cursor.execute(
                            "INSERT INTO punting(playerID, punts, puntYards, grossAvgPuntYards, touchbacks, puntsInside20, longPunt)"
                            "VALUES(?, ?, ?, ?, ?, ?, ?)",
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5])
                        )
                        pass
                    case _: #default 
                        print("received a weird type of data? (switch error)")
                # print(statsheet)
                connection.commit()
