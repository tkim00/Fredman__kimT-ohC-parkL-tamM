# Team Fredman
# SoftDev1 pd09
# Star Trails
# 2020-01-16 due

from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import random
from database import setupDB
import urllib.request as urlrequest
from urllib.request import urlopen, Request
import json

##################################################################################
app = Flask(__name__)
app.secret_key = os.urandom(32) #generates secret key for session
#DB_FILE="database/databases.db"

##################################################################################

# BANDAGES, FOOD, FUEL, MONEY, SHIP PARTS, WEAPONS
#    0        1    2      3        4         5

userData = [0,0,0,0,0,0]

@app.route("/")
def home():
    #Redirect to create character game
    return(redirect(url_for("difficulty")))

@app.route("/")
def difficulty():
    #Choose difficulty
    

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


if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port = '5000', debug = True)
