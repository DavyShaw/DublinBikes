import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
#import simplejson as json
import requests
import time
#from IPython.display import display

URI = "dublinbikes.cns5jzditmzn.us-west-2.rds.amazonaws.com" #link to AWS hosted RDS
PORT = "3306" #default port on RDS
DB = "dublinbikes" #simple DB name - not built for security
USER = "dublinbikes" # simple user name - not built for security
PASSWORD="dublinbikes" #simple password - not built for security

engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

#creates database table - station

sql = """
CREATE TABLE IF NOT EXISTS station (
number INTEGER,
name VARCHAR(256),
position_lat REAL,
position_lng REAL,
status VARCHAR(256),
bike_stands INTEGER
)

"""
try:
    res = engine.execute("DROP TABLE IF EXISTS station")
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)


#creates database table - availability

sql = """
CREATE TABLE IF NOT EXISTS availability (
number INTEGER,
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update INTEGER
)
"""
try:
    res = engine.execute("DROP TABLE IF EXISTS availability")
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)#, traceback.format_exc())


#creates database table - weather

sql = """
CREATE TABLE IF NOT EXISTS weather (
id INTEGER,
city VARCHAR(256),
temp REAL,
temp_max REAL,
temp_min REAL,
humid INT,
pressure INT,
sky INT,
time INT,
)
"""
try:
    res = engine.execute("DROP TABLE IF EXISTS weather")
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)#, traceback.format_exc())
