# Team Fredman
# SoftDev1 pd09
# Star Trails
# 2020-01-16 due

from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
from os import system
import random
import ultimate
#import urllib.request as urlrequest
#from urllib.request import urlopen, Request
import json

##################################################################################
app = Flask(__name__)
app.secret_key = os.urandom(32) #generates secret key for session
#DB_FILE="database/databases.db"

##################################################################################

# BANDAGES, FOOD, FUEL, MONEY, SHIP PARTS, WEAPONS
#     0       1    2      3        4         5
userInventory = [100,100,0,100,100,100]

def changeMoney():
    return None

def changeFood():
    return None

def changeFuel():
    return None

def changeShipParts():
    return None

def changeBandages():
    return None

def changeWeapons():
    return None



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
crewStatus = [300, 100, 100, 100]

passedEncounter = True

############################################################################
############################################################################
# GAME SETUP

@app.route("/")
def home():
    #Redirect to create character game
    return(redirect(url_for("chooseYourDifficulty")))

@app.route("/difficulty")
def chooseYourDifficulty(): #Choose difficulty
    system("cls")
    print( "Choose your difficulty: \n0. Easy\n1. Medium\n2. Hard")
    response = askUser()
    print("RESPONSE: " + str(response))
    global userData
    global userInventory
    if (response == 0):
        print("Easy Mode Selected")
        userInventory[3] = 1500
    elif (response == 1):
        print("Medium Mode Selected")
        userInventory[3] = 1000
    elif (response == 2):
        print("Hard Mode Selected")
        userInventory[3] = 500
    else:
        return difficulty()
    userData[0] = response
    print(userInventory)
    print(userData)
    return chooseYourName()
    #return(redirect(url_for("chooseYourName")))

@app.route("/name")
def chooseYourName(): #Choose your character name
    system("cls")
    print("Choose your character name: ")
    response = input()
    try:
        name = int(response)
        return chooseYourName()
    except:
        global userData
        userData[1] = response
        print(userData)
        return chooseYourCrew()
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
        print(userData)
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

def encounter():
    return exampleEncounter()

def exampleEncounter():
    print("Nothing happened today.\n0. Ok\n")
    response = askUser()
    while (response != 0):
        response = askUser()
    return None


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
    system("cls")
    print("Crew Status:")
    print("Hunger: " + str(crewStatus[0]))
    print("Energy: " + str(crewStatus[1]))
    print("Health: " + str(crewStatus[2]))
    print("Ship Health: " + str(crewStatus[3]) + "\n")
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


# crewStatus
#  food    speed  bandages
# HUNGER, ENERGY, HEALTH, SHIP HEALTH
#   0       1       2         3
#crewStatus = [300, 100, 100, 100]
hungryMessage = True
starvingMessage = True
lowFuelMessage = True
criticalLowFuelMessage = True
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

    if (userSettings[0] == "Meager"):
        if (userInventory[1] >= 10):
            userInventory[1] -= 10
            if (crewStatus[0] >= 30): crewStatus[0] -= 30
            else: crewStatus[0] = 0
        else: crewStatus -= 10
    if (userSettings[0] == "Normal"):
        if (userInventory[1] >= 20):
            userInventory[1] -= 20
        else: crewStatus[0] -= 10
    if (userSettings[0] == "Banquet"):
        if (userInventory[1] >= 30):
            userInventory[1] -= 30
            if (crewStatus[0] <= 350):crewStatus[0] += 30
        else: crewStatus[0] -= 10


    if (crewStatus[0] <= 100 and hungryMessage == True):
        hungryMessage = False
        system("cls")
        print("Your crew is getting hungry.\n0. Continue")
        response = askUser()
        while (response != 0): response = askUser()
    if (crewStatus[0] <= 0 and starvingMessage == True):
        starvingMessage = False
        system("cls")
        print("Your crew is starving.")
        response = askUser()
        while (response != 0): response = askUser()
    if (crewStatus[0] <= 0 and starvingMessage == False):
        print([userData[1]] + " has died of starvation.\n0. Continue")
        while (response != 0): response = askUser()
    if (crewStatus[0] > 0): starvingMessage = True
    if (crewStatus[0] > 100): hungryMessage = True

    if (userSettings[1] == "Slow"): #2 mi/g
        if (userInventory[2] >= 5): userInventory[2] -= 5
        userJourney[1] += 10
        if (crewStatus[1] <= 95): crewStatus[1] += 5
    if (userSettings[1] == "Steady"): #/1.7 mi/g
        if (userInventory[2] >= 10): userInventory[2] -= 10
        userJourney[1] += 17
    if (userSettings[1] == "Fast"): #1.5 mi/g
        if (userInventory[2] >= 20): userInventory[2] -= 20
        userJourney[1] += 30
        if (crewStatus[1] >= 5): crewStatus[1] -= 5

    if (userInventory[2] <= 60 and lowFuelMessage == True):
        lowFuelMessage = False
        system("cls")
        print("Your fuel is running low.\n0. Continue")
        response = askUser()
        while (response != 0): response = askUser()
    if (userInventory[2] <= 0 and criticalLowFuelMessage == True):
        criticalLowFuelMessage = False
        system("cls")
        print("Your fuel is at critical levels.")
        response = askUser()
        while (response != 0): response = askUser()
    if (userInventory[2] <= 0 and criticalLowFuelMessage == False):
        crewStatus[3] -= 10
        print("Your ship has been damaged due to low fuel.\n0. Continue")
        response = askUser()
        while (response != 0): response = askUser()
    if (userInventory[2] > 0): lowFuelMessage = True
    if (userInventory[2] > 60): criticalLowFuelMessage = True

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


chooseYourDifficulty()

#if __name__ == "__main__":
#    app.debug = True
#    app.run()
