from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
from os import system
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

@app.route("/")
def main():
    return render_template('homescreen.html')

@app.route("/game")
def game():
    return render_template('gamescreen.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    return redirect(url_for('login'))

@app.route("/stats")
def stats():
    return render_template('stats.html')
if __name__ == "__main__":
   app.debug = True
   app.run()
