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
from urllib.request import urlopen, Request
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

@app.route("/stats")
def stats():
    if('username' in session and 'password' in session):
        return render_template('stats.html')
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
    return render_template("login.html", error="")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        if('signsub' in request.form):
            # print(request.form)
            session['username'] = request.form["username"]
            session['password'] = request.form["password"]
            session['password1'] = request.form["password1"]
            if(session['password'] == session['password1']):
                return redirect(url_for("main"))
            else:
                return render_template("signup.html", error="Passwords Don't Match")
    return render_template("signup.html", error="")


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

@app.route("/shop1", methods=['GET','POST'])
def chooseYourCrew():
    crew0 = request.form['input0']
    crew1 = request.form['input1']
    crew2 = request.form['input2']
    userData[2] = crew0
    userData[3] = crew1
    userData[4] = crew2
    return render_template("shop.html",
        stat = userInventory)
    #return(redirect(url_for("shop")))

@app.route("/shop", methods=['GET','POST'])
def shop():
    system("cls")
    global userInventory
    print("What would you like to do?")
    print("0. Buy Ship Parts         1. Sell Ship Parts")
    print("2. Buy Fuel               3. Sell Fuel")
    print("4. Buy Food               5. Sell Food")
    print("6. Buy Bandages           7. Sell Bandages")
    print("8. Buy Weapons            9. Sell Weapons")
    print("10. Continue\n")
    #print(message)
    print("Balance: " + str(userInventory[3]))
    print("Ship parts: " + str(userInventory[4]))
    print("Fuel: " + str(userInventory[2]))
    print("Food: " + str(userInventory[1]))
    print("Bandages: " + str(userInventory[0]))
    print("Weapons: " + str(userInventory[5]) + "\n")

    response = int(request.form['input'])
    if (response == 10):
        return render_template("gamescreen.html", day = str(userJourney[0]))
    if (response % 2):
        #print("ODD NUMBER")
        if (response == 1): #SHIP PARTS
            if (userInventory[4] < 50): return render_template("shop.html", message = "Invalid request. Ship parts too low.",stat = userInventory)
            userInventory[3] += 50
            userInventory[4] -= 50
        if (response == 3): #FUEL
            if (userInventory[2] < 50): return render_template("shop.html", message = "Invalid request. Fuel too low.", stat = userInventory)
            userInventory[3] += 50
            userInventory[2] -= 50
        if (response == 5): #FOOD
            if (userInventory[1] < 50): return render_template("shop.html", message = "Invalid request. Food too low.", stat = userInventory)
            userInventory[3] += 50
            userInventory[1] -= 50
        if (response == 7): #Bandages
            if (userInventory[0] < 50): return render_template("shop.html", message = "Invalid request. Bandages too low.", stat = userInventory)
            userInventory[3] += 50
            userInventory[0] -= 50
        if (response == 9): #WEAPONS
            if (userInventory[5] < 50): return render_template("shop.html", message = "Invalid request. Weapons too low.", stat = userInventory)
            userInventory[3] += 50
            userInventory[5] -= 50
    else:
        #print("EVEN NUMBER")
        if (userInventory[3] < 50):
            return render_template("shop.html", message = "Invalid request. Funds too low.", stat = userInventory)
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
    return render_template("shop.html",
        stat = userInventory)



@app.route("/return", methods=['GET','POST'])
def returnToGame():
    return render_template("gamescreen.html", day = str(userJourney[0]))

############################################################################
############################################################################
# PLAY GAME
# userJourney
#  DAY, TRAVELED, PLANET 0, PLANET 1, PLANET 2, PLANET 3, FINISH
#   0      1         2         3         4        5         6
@app.route("/game", methods=['GET','POST'])
def game():
    global passedEncounter

    print("Day " + str(userJourney[0]))
        #PLANET 0
    if (userJourney[1] >= userJourney[2]):
        print("PLANET 0")
        return render_template("/planet")
        userJourney[2] += 1000
    #PLANET 1
    if (userJourney[1] >= userJourney[3]):
        print("PLANET 1")
        return render_template("/planet")
        userJourney[3] += 1000
    #PLANET 2
    if (userJourney[1] >= userJourney[4]):
        print("PLANET 2")
        return render_template("/planet")
        userJourney[4] += 1000
    #PLANET 3
    if (userJourney[1] >= userJourney[5]):
        print("PLANET 3")
        return render_template("/planet")
        userJourney[5] += 1000
    #FINISH
    if (userJourney[1] >= userJourney[6]):
        print("Congratulations! You have finished the game")
        return render_template("/fin")
        #return endScreen()

        #return endScreen()
    ######################
    #print("Day " + str(userJourney[0]))
    #print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings")
    #INVENTORY AND CREW STATUS
    response = int(request.form["input"])
    while (response != 0):
        if (response == 1): return render_template("inventory.html", stat = userInventory)
        if (response == 2): return render_template("crewStatus.html", crewStat = crewStatus, crewMessages = statusMessages)
        if (response == 3): return render_template("settings.html", settings = userSettings)
        print("Day " + str(userJourney[0]))
        print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings")
        return returnToGame()
        #response = askUser()

    userJourney[0] += 1
    dayPasses()
    print(passedEncounter)
    return encounter()

def planet1():
    link = urlopen("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&pl_name")
    response = link.read()
    #data = json.loads( response )
    return response[0]


# crewStatus
#  food    speed  bandages
# HUNGER, ENERGY, HEALTH, SHIP HEALTH
#   0       1       2         3
#crewStatus = [300, 100, 100, 100]
def encounter():
    global crewStatus
    #determine which aspect
    typeEncounter = random.randint(0,3)
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
    #if (typeEncounter == 4):
    #    result = DBMethods.getSituations()[0]
    #    return result[0]

    char = userData[random.randint(1,4)]
    print("0. Continue")
    return render_template("encounter.html", day = userJourney[0], char = char, result = result)

def planet():
    print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings\n4. Shop")
    response = askUser()
    while (response != 0):
        if (response == 1): inventory()
        if (response == 2): status()
        if (response == 3): settings()
        if (response == 4): shop("Welcome to Connor's Shop! What would you like to do?")
        system("cls")
        print("Day " + userJourney[0])
        print("0. Continue\n1. Inventory\n2. Crew Status\n3. Settings\n4. Shop")
        response = askUser()
        return("YES")
    return("YES")



@app.route("/changeSettings", methods=['GET','POST'])
def changeSettings():
    response = int(request.form["input"])
    while (response != 6):
        if (response == 0): userSettings[0] = "Meager"
        if (response == 1): userSettings[0] = "Normal"
        if (response == 2): userSettings[0] = "Banquet"
        if (response == 3): userSettings[1] = "Slow"
        if (response == 4): userSettings[1] = "Steady"
        if (response == 5): userSettings[1] = "Fast"
        return render_template("settings.html", settings = userSettings)
    return returnToGame()

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
    return ("worked")


print(planet1())

#if __name__ == "__main__":
#    app.debug = True
#    app.run()
