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

def nasaAPI():
    link = urlopen("https://images-api.nasa.gov/search?q=planet")
    response = link.read()
    data = json.loads( response )
    return data['collection']['items'][random.randint(0,100)]['links'][0]['href']

print(nasaAPI())
