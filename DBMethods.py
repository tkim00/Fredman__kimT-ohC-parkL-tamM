import sqlite3   #enable control of an sqlite database

DB_FILE="ultimate.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops


# HELPER METHODS

#    1. get table data from DB
def getTableData(table, command):
    DB_FILE="ultimate.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops
    rowList = []
    getRow = c.execute(command.format(table))
    tableData = getRow.fetchall()
    for row in tableData:
        rowList.append([ item for item in row ])
    return rowList

#    2. get easy visual of DB list
def visualList(getStuff):
    DB_FILE="ultimate.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    for i in getStuff:
        print (i)
    print ("number of objects in list: " + str(len(getStuff)))

#    3. check if info already in DB
#         if in DB, returns TRUE
#         if username not in DB or password is wrong, returns FALSE
def checkLogin(username, password):
     command = " SELECT * FROM {}; "
     userData = getTableData('userStuff', command)
     x = 0
     while x < len(userData):
          if username == userData[x][0]:
               if password == userData[x][1]:
                    return True
          x += 1
     return False # not in DB

#    4. add row in userStuff in DB (sign up new users)

def checkSignUp(username, password):
    if checkLogin(username, password): return False;
    else: return True;

def signUp(usrnme, pswrd):
    db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops
    command = " INSERT INTO userStuff VALUES ('{}', '{}'); ".format(usrnme, pswrd)
    c.execute(command)
    db.commit()
    db.close()



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

signUp('bob', 'joe')
#print checkLogin('admin', 'admin')
#print getSituations()[0]
#visualList(getNormShipHealth()[0])
#hey = "SELECT * FROM {}"
#y = getTableData('userStuff', hey)
#x = 0
#while x < len(y):
#                 print y[x][1]
#                 x += 1
#print getTableData('userStuff',hey)[0][0]
print(getSituations()[0][0])
