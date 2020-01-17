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

def hubbleAPI():
    id = random.randint(0,1000)
    link = urlopen("http://hubblesite.org/api/v3/image/{}".format(id))
    response = link.read()
    data = json.loads( response )
    print(data)
    return data["image_files"][4]["file_url"]
