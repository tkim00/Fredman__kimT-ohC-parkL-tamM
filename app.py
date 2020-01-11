# Team Fredman
# SoftDev1 pd09
# Star Trails
# 2020-01-16 due

from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import random
#from database import setupDB
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
userEquipment = [0,0,0,0,0,0]

# DIFFICULTY, NAME, CREW0, CREW1, CREW2,
#     0        1      2      3      4
userData = [0,"name","crew0","crew1","crew2"]

@app.route("/")
def home():
    #Redirect to create character game
    return(redirect(url_for("chooseYourDifficulty")))

@app.route("/difficulty")
def chooseYourDifficulty(): #Choose difficulty
    print( "Choose your difficulty: \n0. Easy\n1. Medium\n2. Hard")
    response = askUser()
    print("RESPONSE: " + str(response))
    global userData
    global userEquipment
    if (response == 0):
        print("Easy Mode Selected")
        userEquipment[3] = 3000
    elif (response == 1):
        print("Medium Mode Selected")
        userEquipment[3] = 2000
    elif (response == 2):
        print("Hard Mode Selected")
        userEquipment[3] = 1000
    else:
        return difficulty()
    userData[0] = response
    print(userEquipment)
    print(userData)
    #return(redirect(url_for("chooseYourName")))

@app.route("/name")
def chooseYourName(): #Choose your character name
    print("Choose your character name: ")
    response = input()
    try:
        name = int(response)
        return chooseYourName()
    except:
        global userData
        userData[1] = response
        print(userData)
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
    #return(redirect(url_for("shop")))

@app.route("/shop")
def shop(message):
    global userEquipment
    print("What would you like to do?")
    print("0. Buy Ship Parts         1. Sell Ship Parts")
    print("2. Buy Fuel               3. Sell Fuel")
    print("4. Buy Food               5. Sell Food")
    print("6. Buy Bandages           7. Sell Bandages")
    print("8. Buy Weapons            9. Sell Weapons")
    print("10. Continue\n")
    print(message)
    print("Balance: " + str(userEquipment[3]))
    print("Ship parts: " + str(userEquipment[4]))
    print("Fuel: " + str(userEquipment[2]))
    print("Food: " + str(userEquipment[1]))
    print("Bandages: " + str(userEquipment[0]))
    print("Weapons: " + str(userEquipment[5]) + "\n")

    response = askUser()
    if (response % 2):
        #print("ODD NUMBER")
        if (response == 1): #SHIP PARTS
            if (userEquipment[4] < 50): return shop("Invalid request. Ship parts too low.")
            userEquipment[3] += 50
            userEquipment[4] -= 50
        if (response == 3): #FUEL
            if (userEquipment[2] < 50): return shop("Invalid request. Fuel too low.")
            userEquipment[3] += 50
            userEquipment[2] -= 50
        if (response == 5): #FOOD
            if (userEquipment[1] < 50): return shop("Invalid request. Food too low.")
            userEquipment[3] += 50
            userEquipment[1] -= 50
        if (response == 7): #Bandages
            if (userEquipment[0] < 50): return shop("Invalid request. Bandages too low.")
            userEquipment[3] += 50
            userEquipment[0] -= 50
        if (response == 9): #WEAPONS
            if (userEquipment[5] < 50): return shop("Invalid request. Weapons too low.")
            userEquipment[3] += 50
            userEquipment[5] -= 50
    else:
        #print("EVEN NUMBER")
        if (userEquipment[3] < 50):
            return shop("Invalid request. Funds too low.")
        if (response == 0): #SHIP PARTS
            userEquipment[3] -= 50
            userEquipment[4] += 50
        if (response == 2): #FUEL
            userEquipment[3] -= 50
            userEquipment[2] += 50
        if (response == 4): #FOOD
            userEquipment[3] -= 50
            userEquipment[1] += 50
        if (response == 6):
            userEquipment[3] -= 50
            userEquipment[0] += 50
        if (response == 8):
            userEquipment[3] -= 50
            userEquipment[5] += 50
        if (response == 10):
            print("continue")
    print(userEquipment)
    return shop("")


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


shop("")

#if __name__ == "__main__":
#    app.debug = True
#    app.run()
