import requests, json, os, re, sqlite3
from pathlib import Path

game_url = "https://www.espn.com/nfl/boxscore/_/gameId/401872995"
gameHtml = requests.get(game_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text

marker = re.compile(r"window\['__espnfitt__'\]\s*=\s*")

connection = sqlite3.connect("football.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
cursor.executescript(schema)

def seperateFraction(str):
    numerator = re.compile(r"\d+(?=/)")
    denominator = re.compile(r"(?<=/)+\d+")
    num = re.search(numerator, str)
    denom = re.search(denominator, str)
    return {num, denom}

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
        
                playerItem = loadPlayerFromHtml(playerHtml)
                cursor.execute(
                    "INSERT INTO players(playerID, name, position, team, age) VALUES (?, ?, ?, ?, ?)"
                    "ON CONFLICT(playerID) DO NOTHING", # if the player was already loaded, leave it be.
                    (playerID, name, playerItem["plyrHdr"]["ath"]["posAbv"], playerItem["plyrHdr"]["ath"]["tm"], playerItem["plyrHdr"]["ath"]["dob"]),
                )
                
                match (s[0] if s else None):
                    case "completions/passingAttempts":
                        cursor.execute("""(
                            INSERT INTO passing(playerID, completions, pAttempts, pYards, YPPA, pTouchdowns, ints, sacks, YLtoSacks, adjQBR, QBR)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]), 
                                )
                                    """)
                        pass
                    case "receptions":
                        cursor.execute("""(
                            INSERT INTO receiving(playerID, receptions, rYards, YPR, rTouchdowns, fumbles)
                            VALUES(?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4]), 
                                )
                                    """)
                        pass
                    case "fumbles":
                        cursor.execute("""(
                            INSERT INTO fumbles(playerID, fumbles, fumblesLost)
                            VALUES(?, ?, ?),
                            (playerID, p[0], p[1]), 
                                )
                                    """)
                        pass
                    case "totalTackles":
                        cursor.execute("""(
                            INSERT INTO defense(playerID, totalTackles, soloTackles, assists, sacks, YLtoSacks, tacklesForLoss, YLtoTFL, passesDefended, interceptions, kickReturns, puntReturns, fieldGoalsMade/fieldGoalAttempts)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]), 
                                )
                                    """)
                        pass
                    case "interceptions":
                        cursor.execute("""(
                            INSERT INTO defense(playerID, totalTackles, soloTackles, assists, sacks, YLtoSacks, tacklesForLoss, YLtoTFL, passesDefended, interceptions, kickReturns, puntReturns, fieldGoalsMade/fieldGoalAttempts)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]), 
                                )
                                    """)
                        pass
                    case "kickReturns":
                        cursor.execute("""(
                            INSERT INTO defense(playerID, totalTackles, soloTackles, assists, sacks, YLtoSacks, tacklesForLoss, YLtoTFL, passesDefended, interceptions, kickReturns, puntReturns, fieldGoalsMade/fieldGoalAttempts)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]), 
                                )
                                    """)
                        pass
                    case "puntReturns":
                        cursor.execute("""(
                            INSERT INTO defense(playerID, totalTackles, soloTackles, assists, sacks, YLtoSacks, tacklesForLoss, YLtoTFL, passesDefended, interceptions, kickReturns, puntReturns, fieldGoalsMade/fieldGoalAttempts)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]), 
                                )
                                    """)
                        pass
                    case "fieldGoalsMade/fieldGoalAttempts":
                        cursor.execute("""(
                            INSERT INTO defense(playerID, totalTackles, soloTackles, assists, sacks, YLtoSacks, tacklesForLoss, YLtoTFL, passesDefended, interceptions, kickReturns, puntReturns, fieldGoalsMade/fieldGoalAttempts)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?),
                            (playerID, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]), 
                                )
                                    """)
                        pass
                    case _: #default 
                        print("received a weird type of data? (switch error)")
                # print(statsheet)
                connection.commit()
