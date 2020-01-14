import sqlite3   #enable control of an sqlite database

DB_FILE="ultimate.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

# HELPER METHOD = get table data from DB
def getTableData(table):
     rowList = []
     getRowCommand = " SELECT * FROM {} ORDER BY RANDOM() LIMIT 1; ".format(table)
     getRow = c.execute(getRowCommand)
     tableData = getRow.fetchall()
     for row in tableData:
          for i in row:
               rowList.append(i)
     return rowList

# SINGLE CREW MEMBER ENCOUNTERS
# returns [criteria, encounter, result]
#    CRITERIA: for reference
#    ENCOUNTER: random crewmember name + encounter
#    RESULT: change selected crewmember status to result
def getEncounters():
     return getTableData('userencounters')

# INVENTORY-AFFECTING SITUATIONS
# returns [prob, situation, result]
#    ENCOUNTER: random crewmember name + encounter
#    RESULT: change selected crewmember status to result
def getSituations():
     return getTableData('situations')
