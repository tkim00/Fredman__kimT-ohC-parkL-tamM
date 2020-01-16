# Team Fredman
# SoftDev1 pd09
# Star Trails
# 2020-01-16 due

from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
from os import system
import random
import DBMethods
#from database import setupDB
#import urllib.request as urlrequest
#from urllib.request import urlopen, Request
import json

##################################################################################
app = Flask(__name__)
app.secret_key = os.urandom(32) #generates secret key for session
DB_FILE="ultimate.db"

##################################################################################

# BANDAGES, FOOD, FUEL, MONEY, SHIP PARTS, WEAPONS
#     0       1    2      3        4         5
userInventory = [200,200,200,1000,200,200]

# DIFFICULTY, NAME, CREW0, CREW1, CREW2,
#     0        1      2      3      4
userData = [0,"name","crew0","crew1","crew2"]

# USER SETTINGS
#  FOOD(TXT), SPEED(TXT), FOOD(LVL), SPEED(LVL)
#   0             1            2            3
userSettings = ["Normal","Steady", 1, 1]

# userJourney
#  DAY, TRAVELED, PLANET 1, PLANET 2, PLANET 3, PLANET 4, FINISH
#   0      1         2         3         4        5         6
userJourney = [0,0,40,100,150,225,300]

# crewStatus
#  food    speed  bandages
# HUNGER, ENERGY, HEALTH, SHIP HEALTH
#   0       1       2         3
crewStatus = [200, 100, 100, 100]

passedEncounter = True

#STATUS MESSAGES IN crewStatus
# HUNGER, HEALTH, Ship HEALTH
#   0       1         2
statusMessages = ['','','']

############################################################################
############################################################################
# GAME SETUP

@app.route("/home", methods=["GET"])
def main():
    if('username' in session and 'password' in session):
        return render_template('homescreen.html')
    return(redirect(url_for("login")))

@app.route("/start")
def start():
    return render_template('gamescreen.html')

@app.route("/logout")
def logout():
    session.pop('username')
    session.pop('password')
    return redirect(url_for('login'))

@app.route("/crewstats")
def stats():
    if('username' in session and 'password' in session):
        return render_template('crewstats.html')
    return(redirect(url_for("login")))

@app.route("/")
def home():
    #Redirect to create character game
    if('username' in session and 'password' in session):
        return redirect(url_for("main"))
    return(redirect(url_for("login")))

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if('loginsub' in request.form):
            # print(request.form)
            session['username'] = request.form["username"]
            session['password'] = request.form["password"]
            return redirect(url_for("main"))
    return render_template("login.html")

@app.route("/signup")
def signup():
    if request.method == 'POST':
        if('signsub' in request.form):
            # print(request.form)
            session['username'] = request.form["username"]
            session['password'] = request.form["password"]
            return redirect(url_for("main"))
    return render_template("signup.html")


@app.route("/startGame")
def startGame():
    print("STARTGAME!!!")
    return render_template("difficulty.html")

@app.route("/name", methods=['GET','POST'])
def chooseYourDifficulty(): #Choose difficulty
    print("HERE!!!")
    print(request.form['input'])
    response = int(request.form['input'])
    global userData
    global userInventory
    if (response == 0):
        userInventory[3] = 1500
    elif (response == 1):
        userInventory[3] = 1000
    elif (response == 2):
        userInventory[3] = 500
    else: return "Broke"
    userData[0] = response
    print(userInventory)
    print(userData)
    return render_template("name.html")

@app.route("/crew", methods=['GET','POST'])
def chooseYourName(): #Choose your character name
    response = request.form['input']
    try:
        name = int(response)
        return redirect(url_for(chooseYourDifficulty))
    except:
        global userData
        userData[1] = response
        return render_template("crew.html")
        #return(redirect(url_for("chooseYourCrew")))

@app.route("/crew")
def chooseYourCrew():
    print("Create your crew: ")
    int = 0
    while (int < 3):
        print("Character " + str(int) + ":")
        response = input()
        global userData
        userData[int + 2] = response
        int += 1
    return shop("")
    #return(redirect(url_for("shop")))

@app.route("/shop")
def shop(message):
    system("cls")
    global userInventory
    print("What would you like to do?")
    print("0. Buy Ship Parts         1. Sell Ship Parts")
    print("2. Buy Fuel               3. Sell Fuel")
    print("4. Buy Food               5. Sell Food")
    print("6. Buy Bandages           7. Sell Bandages")
    print("8. Buy Weapons            9. Sell Weapons")
    print("10. Continue\n")
    print(message)
    print("Balance: " + str(userInventory[3]))
    print("Ship parts: " + str(userInventory[4]))
    print("Fuel: " + str(userInventory[2]))
    print("Food: " + str(userInventory[1]))
    print("Bandages: " + str(userInventory[0]))
    print("Weapons: " + str(userInventory[5]) + "\n")

    response = askUser()
    if (response == 10):
        game()
    if (response % 2):
        #print("ODD NUMBER")
        if (response == 1): #SHIP PARTS
            if (userInventory[4] < 50): return shop("Invalid request. Ship parts too low.")
            userInventory[3] += 50
            userInventory[4] -= 50
        if (response == 3): #FUEL
            if (userInventory[2] < 50): return shop("Invalid request. Fuel too low.")
            userInventory[3] += 50
            userInventory[2] -= 50
        if (response == 5): #FOOD
            if (userInventory[1] < 50): return shop("Invalid request. Food too low.")
            userInventory[3] += 50
            userInventory[1] -= 50
        if (response == 7): #Bandages
            if (userInventory[0] < 50): return shop("Invalid request. Bandages too low.")
            userInventory[3] += 50
            userInventory[0] -= 50
        if (response == 9): #WEAPONS
            if (userInventory[5] < 50): return shop("Invalid request. Weapons too low.")
            userInventory[3] += 50
            userInventory[5] -= 50
    else:
        #print("EVEN NUMBER")
        if (userInventory[3] < 50):
            return shop("Invalid request. Funds too low.")
        if (response == 0): #SHIP PARTS
            userInventory[3] -= 50
            userInventory[4] += 50
        if (response == 2): #FUEL
            userInventory[3] -= 50
            userInventory[2] += 50
        if (response == 4): #FOOD
            userInventory[3] -= 50
            userInventory[1] += 50
        if (response == 6):
            userInventory[3] -= 50
            userInventory[0] += 50
        if (response == 8):
            userInventory[3] -= 50
            userInventory[5] += 50

    #print(userInventory)
    return shop("")

############################################################################
############################################################################
# PLAY GAME
# userJourney
#  DAY, TRAVELED, PLANET 0, PLANET 1, PLANET 2, PLANET 3, FINISH
#   0      1         2         3         4        5         6
@app.route("/game")
def game():
    global passedEncounter

    system("cls")
    print("Day " + str(userJourney[0]))

    #PLANET 0
    if (userJourney[1] >= userJourney[2]):
        print("PLANET 0")
        planet()
        userJourney[2] += 1000
    #PLANET 1
    if (userJourney[1] >= userJourney[3]):
        print("PLANET 1")
        planet()
        userJourney[3] += 1000
    #PLANET 2
    if (userJourney[1] >= userJourney[4]):
        print("PLANET 2")
        planet()
        userJourney[4] += 1000
    #PLANET 3
    if (userJourney[1] >= userJourney[5]):
        print("PLANET 3")
        planet()
        userJourney[5] += 1000
    #FINISH
    if (userJourney[1] >= userJourney[6]):
        print("Congratulations! You have finished the game")
        exit()
        #return endScreen()
    #ENCOUNTER
    if (passedEncounter == False):
        passedEncounter = True
        encounter()
    passedEncounter = False

    ######################

    system("cls")
    print("Day " + str(userJourney[0]))
    print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings")
    #INVENTORY AND CREW STATUS
    response = askUser()
    while (response != 0):
        if (response == 1): inventory()
        if (response == 2): status()
        if (response == 3): settings()
        system("cls")
        print("Day " + str(userJourney[0]))
        print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings")
        response = askUser()

    userJourney[0] += 1
    dayPasses()

    return game()

# crewStatus
#  food    speed  bandages
# HUNGER, ENERGY, HEALTH, SHIP HEALTH
#   0       1       2         3
#crewStatus = [300, 100, 100, 100]
def encounter():
    global crewStatus
    #determine which aspect
    typeEncounter = random.randint(0,4)
    #HUNGER
    if (typeEncounter == 0):
        if (crewStatus[0] >= 50):
            result = DBMethods.getNormHunger()[random.randint(0,5)]
        else:
            result = DBMethods.getLowHunger()[random.randint(0,2)]
    #ENERGY
    if (typeEncounter == 1):
        if (crewStatus[1] >= 20):
            result = DBMethods.getNormEnergy()[random.randint(0,1)]
        else:
            result = DBMethods.getLowEnergy()[random.randint(0,4)]
    #HEALTH
    if (typeEncounter == 2):
        if (crewStatus[2] >= 20):
            result = DBMethods.getNormHealth()[random.randint(0,1)]
        else:
            result = DBMethods.getLowHealth()[random.randint(0,3)]
    #SHIP HEALTH
    if (typeEncounter == 3):
        if (crewStatus[3] >= 20):
            result = DBMethods.getNormShipHealth()[random.randint(0,2)]
        else:
            result = DBMethods.getLowShipHealth()[random.randint(0,2)]
    #SPECIAL ENCOUNTER: SITUATION
    if (typeEncounter == 4):
        result = DBMethods.getSituations()[0]
        return print(result[0])

    system("cls")
    print("Day " + str(userJourney[0]))
    char = userData[random.randint(1,4)]
    print(char + " " + result[1])
    print("0. Continue")
    response = askUser()
    while (response != 0):
        response = askUser()
    print("GO ONTO GAME")

def planet():
    print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings\n4. Shop")
    response = askUser()
    while (response != 0):
        if (response == 1): inventory()
        if (response == 2): status()
        if (response == 3): settings()
        if (response == 4): shop("Welcome to Connor's Shop! What would you like to do?")
        system("cls")
        print("Day " + str(userJourney[0]))
        print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings\n4. Shop")
        response = askUser()


# BANDAGES, FOOD, FUEL, MONEY, SHIP PARTS, WEAPONS
#     0       1    2      3        4         5
def inventory():
    system("cls")
    print("Current Inventory:")
    print("Bandages: " + str(userInventory[0]))
    print("Food: " + str(userInventory[1]))
    print("Fuel: " + str(userInventory[2]))
    print("Money: " + str(userInventory[3]))
    print("Ship Parts: " + str(userInventory[4]))
    print("Weapons: " + str(userInventory[5]) + "\n")
    print("0. Continue\n")
    response = askUser()
    if (response != 0): return inventory()
    return None

def status():
    global statusMessages
    system("cls")
    print("Crew Status:")
    print("Hunger: " + str(crewStatus[0]))
    print("Energy: " + str(crewStatus[1]))
    print("Health: " + str(crewStatus[2]))
    print("Ship Health: " + str(crewStatus[3]) + "\n")
    print(statusMessages[0])
    print(statusMessages[1])
    print(statusMessages[2])
    print("0. Continue\n")
    response = askUser()
    while (response != 0): return crewStatus()
    return None

# USER SETTINGS
#  FOOD(TXT), SPEED(TXT),
#   0             1
def settings():
    system("cls")
    print("Current Settings:")
    print("Food: " + userSettings[0])
    print("Speed: " + userSettings[1] + "\n")
    print("0. Meager   1. Normal     2. Banquet")
    print("3. Slow     4. Steady     5. Fast\n")
    print("6. Continue\n")
    response = askUser()
    while (response != 6):
        if (response == 0): userSettings[0] = "Meager"
        if (response == 1): userSettings[0] = "Normal"
        if (response == 2): userSettings[0] = "Banquet"
        if (response == 3): userSettings[1] = "Slow"
        if (response == 4): userSettings[1] = "Steady"
        if (response == 5): userSettings[1] = "Fast"
        return settings()
    return None


#STATUS MESSAGES IN crewStatus
# HUNGER, HEALTH, Ship HEALTH
#   0       1         2
#statusMessages = ['','','']

# crewStatus
#  food    speed  bandages
# HUNGER, ENERGY, HEALTH, SHIP HEALTH
#   0       1       2         3
#crewStatus = [200, 100, 100, 100]
def dayPasses():
    global hungryMessage
    global starvingMessage
    global lowFuelMessage
    global criticalLowFuelMessage

    global userSettings
    global userJourney
    global userInventory
    global userData
    global crewStatus

    ###################### FOOD / HUNGER
    if (userSettings[0] == "Meager"):
        if (userInventory[1] >= 10): #any food left?
            userInventory[1] -= 20
            if (crewStatus[0] >= 30): crewStatus[0] -= 30 #any hunger left?
            else: crewStatus[0] = 0
        else: crewStatus -= 10 #damage per day of no food
    if (userSettings[0] == "Normal"):
        if (userInventory[1] >= 20):
            userInventory[1] -= 20
        else: crewStatus[0] -= 20
    if (userSettings[0] == "Banquet"):
        if (userInventory[1] >= 30):
            userInventory[1] -= 30
            if (crewStatus[0] <= 350):crewStatus[0] += 30
        else: crewStatus[0] -= 20

    if (crewStatus[0] > 100):
        statusMessages[1] = ""
    if ((crewStatus[0] <= 100) and (crewStatus[0] > 50)):
        statusMessages[0] = "Your crew is getting hungry."
    if ((crewStatus[0] <= 50) and (crewStatus[0] > 0)):
        statusMessages[0] = "Your crew is pale and thin."
    if (crewStatus[0] == 0):
        statusMessages[0] = "Your crew is starving."
        crewStatus[2] -= 10
    ######################

    ###################### SPEED / ENERGY
    if (userSettings[1] == "Slow"): #2 mi/g
        if (userInventory[2] >= 5):
            userInventory[2] -= 5
            crewStatus[1] += 10
        else: crewStatus[1] -= 15
        userJourney[1] += 10
    if (userSettings[1] == "Steady"): #/1.7 mi/g
        if (userInventory[2] >= 10): userInventory[2] -= 10
        else: crewStatus[1] -= 15
        userJourney[1] += 17
    if (userSettings[1] == "Fast"): #1.5 mi/g
        if (userInventory[2] >= 20):
            userInventory[2] -= 20
            crewStatus[1] -= 10
        else: crewStatus[1] -= 15
        userJourney[1] += 30

    if (crewStatus[1] > 80):
        statusMessages[1] = ""
    if ((crewStatus[1] <= 80) and (crewStatus[1] > 40)):
        statusMessages[1] = "Your crew is getting tired."
    if ((crewStatus[1] <= 40) and (crewStatus[1] > 20)):
        statusMessages[1] = "Your crew is exhausted."
    if (crewStatus[1] <= 0):
        statusMessages[1] = "Your crew has collapsed."
        crewStatus[2] -= 10
    ######################
    return game()

############################################################################
############################################################################
# HELPER METHODS!!!!!!
def askUser():
    #raw_input NOT in python 3
    data = input("Input number: ")
    try:
        num = int(data)
        #print(num)
        return num
    except:
        return askUser()



#chooseYourDifficulty()

if __name__ == "__main__":
    app.debug = True
    app.run()
