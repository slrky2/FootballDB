-- Each stats table stores one row per player for a single dataset.
-- Enable PRAGMA foreign_keys = ON on every connection before starting a transaction.

CREATE TABLE IF NOT EXISTS players (
    playerID INTEGER PRIMARY KEY,
    name TEXT,
    position TEXT,
    team TEXT,
    age INTEGER
);

CREATE TABLE IF NOT EXISTS passing (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    completions INTEGER,
    pAttempts INTEGER,
    pYards INTEGER,
    YPPA REAL,
    pTouchdowns INTEGER,
    ints INTEGER,
    sacks INTEGER,
    YLtoSacks INTEGER,
    adjQBR REAL,
    QBR REAL
);

CREATE TABLE IF NOT EXISTS rushing (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    rAttempts INTEGER,
    rYards INTEGER,
    YPRA REAL,
    rTouchdowns INTEGER,
    longestRush INTEGER
);

CREATE TABLE IF NOT EXISTS receiving (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    receptions INTEGER,
    receivingYards INTEGER,
    yardsPerReception REAL,
    receivingTouchdowns INTEGER,
    longReception INTEGER,
    receivingTargets INTEGER
);

CREATE TABLE IF NOT EXISTS fumbles (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    fumbles INTEGER,
    fumblesLost INTEGER,
    fumblesRecovered INTEGER
);

CREATE TABLE IF NOT EXISTS defense (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    totalTackles INTEGER,
    soloTackles INTEGER,
    sacks REAL,
    tacklesForLoss REAL,
    passesDefended INTEGER,
    QBHits INTEGER,
    defensiveTouchdowns INTEGER
);

CREATE TABLE IF NOT EXISTS defensive_interceptions (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    interceptions INTEGER,
    interceptionYards INTEGER,
    interceptionTouchdowns INTEGER
);

CREATE TABLE IF NOT EXISTS kick_returns (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    kickReturns INTEGER,
    kickReturnYards INTEGER,
    yardsPerKickReturn REAL,
    longKickReturn INTEGER,
    kickReturnTouchdowns INTEGER
);

CREATE TABLE IF NOT EXISTS punt_returns (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    puntReturns INTEGER,
    puntReturnYards INTEGER,
    yardsPerPuntReturn REAL,
    longPuntReturn INTEGER,
    puntReturnTouchdowns INTEGER
);

CREATE TABLE IF NOT EXISTS kicking (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    fieldGoalsMade INTEGER,
    fieldGoalAttempts INTEGER,
    fieldGoalPct REAL,
    longFieldGoalMade INTEGER,
    extraPointsMade INTEGER,
    extraPointAttempts INTEGER,
    totalKickingPoints INTEGER
);

CREATE TABLE IF NOT EXISTS punting (
    playerID INTEGER PRIMARY KEY REFERENCES players(playerID),
    punts INTEGER,
    puntYards INTEGER,
    grossAvgPuntYards REAL,
    touchbacks INTEGER,
    puntsInside20 INTEGER,
    longPunt INTEGER
);
