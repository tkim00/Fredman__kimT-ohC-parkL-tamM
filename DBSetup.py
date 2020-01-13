import sqlite3   #enable control of an sqlite database

DB_FILE="ultimate.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#######################################

# USERS TABLE

#    TABLE BREAKDOWN
#       1 BLOCK = identification to connect databases
#       2 BLOCK = login info
#       3 BLOCK = user's game inventory
#       4 BLOCK = user's game data
#       5 BLOCK = user settings

userTable = """ CREATE TABLE userStuff (

          id INTEGER,
          
          username TEXT,
          password BLOB,
          
          bandages INTEGER,
          food INTEGER,
          fuel INTEGER,
          money INTEGER,
          shipParts INTEGER,
          weapons INTEGER,
          
          day INTEGER,

          difficulty TEXT,
          foodSetting TEXT,
          speedSetting TEXT,
          foodFactor INTEGER,
          speedFactor INTEGER
          
          );"""
#######################################

#######################################

# USER'S TEAM TABLE

#    TABLE BREAKDOWN
#       1 BLOCK = identification to connect databases
#       2 BLOCK = crew members of user
#       3 BLOCK = status of crew members; only important if "dead"

userteamTable = """ CREATE TABLE teams (

          id INTEGER,
          
          name TEXT,
          crew0 TEXT,
          crew1 TEXT,
          crew2 TEXT,

          nameStat TEXT,
          crew0Stat TEXT,
          crew1Stat TEXT,
          crew2Stat TEXT
          
          );"""
#######################################

#######################################

# MEMBER ENCOUNTERS TABLE

#    TABLE BREAKDOWN
#        CRITERIA  = first check if criteria is True
#                       else, go to next encounter
#        PROB      = once criteria is True, if prob is True
#                       else, go to next encounter
#        ENCOUNTER = attach crewmember name in front
#        RESULT    = change crewmember status

"""
ex.   criteria                |   prob   |   encounter          |   result
      foodSetting == "Meager"     0.3        gets cannibalized      dead
      speedSetting == "Fast"      0.4        is exhausted           exhausted
      bandages <= 300             0.2        gets pneumonia         sick
CRITERIA: foodSetting {Meader, Normal, Banquet}
          speedSetting {Slow, Steady, Fast}
          bandages, shipParts
"""

userencounterTable = """ CREATE TABLE userencounters (

          criteria BLOB,
          prob REAL,
          encounter TEXT,
          result TEXT
          
          );"""
#######################################

#######################################

# SITUATIONS TABLE

#    TABLE BREAKDOWN
#        PROB      = integer, choose randomly from range (0,x)
#        SITUATION = print out text
#        RESULT    = change game inventory

"""
ex.   prob   |   situation                                            |   result
      1          The crew encountered a mysterious box. It explodes!      bandages, -200
      2          The starship got attacked by a space squid!              shipParts, -30
"""

situationTable = """ CREATE TABLE situations (

          prob INTEGER,
          situation TEXT,
          result TEXT
          
          );"""
#######################################

c.execute(userTable)
c.execute(userteamTable)
c.execute(userencounterTable)
c.execute(situationTable)

db.commit()
db.close()
