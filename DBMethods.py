import sqlite3   #enable control of an sqlite database

DB_FILE="ultimate.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops


# HELPER METHODS

#    1. get table data from DB
def getTableData(table, command):
     rowList = []
     getRow = c.execute(command.format(table))
     tableData = getRow.fetchall()
     for row in tableData:
          rowList.append([ item for item in row ])
     return rowList

#    2. get easy visual of DB list
def visualList(getStuff):
     for i in getStuff:
          print i
     print "number of objects in list: " + str(len(getStuff))



# LOGIN METHOD



# SINGLE CREW MEMBER ENCOUNTERS

# returns [criteria, encounter, result]
#    CRITERIA: for reference
#    ENCOUNTER: random crewmember name + encounter
#    RESULT: change selected crewmember status to result


#    GET HUNGER ENCOUNTERS
def getLowHunger():
     command = " SELECT * FROM {} LIMIT 3; "
     return getTableData('userencounters', command)

def getNormHunger():
     command = " SELECT * FROM {} LIMIT 3,6; "
     return getTableData('userencounters', command)


#    GET ENERGY ENCOUNTERS
def getLowEnergy():
     command = " SELECT * FROM {} LIMIT 13,5; "
     return getTableData('userencounters', command)

def getNormEnergy():
     command = " SELECT * FROM {} LIMIT 9,4; "
     return getTableData('userencounters', command)


#    GET HEALTH ENCOUNTERS
def getLowHealth():
     command = " SELECT * FROM {} LIMIT 18,4; "
     return getTableData('userencounters', command)

def getNormHealth():
     command = " SELECT * FROM {} LIMIT 22,2; "
     return getTableData('userencounters', command)


#    GET SHIP HEALTH ENCOUNTERS
def getLowShipHealth():
     command = " SELECT * FROM {} LIMIT 27,3; "
     return getTableData('userencounters', command)

def getNormShipHealth():
     command = " SELECT * FROM {} LIMIT 24,3; "
     return getTableData('userencounters', command)



# INVENTORY-AFFECTING SITUATIONS

# returns [situation, result]
#    ENCOUNTER: random crewmember name + encounter
#    RESULT: change selected crewmember status to result

def getSituations():
     getRandRow = " SELECT * FROM {} ORDER BY RANDOM() LIMIT 1; "
     return getTableData('situations', getRandRow)



# TEST
visualList(getLowShipHealth())

