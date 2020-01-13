# Team Fredman
# SoftDev1 pd09
# Star Trails
# 2020-01-16 due

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
