import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
#import simplejson as json
import requests
import time
#from IPython.display import display

def accessDB():
    URI = "dublinbikes.cns5jzditmzn.us-west-2.rds.amazonaws.com" #link to AWS hosted RDS
    PORT = "3306" #default port on RDS
    DB = "dublinbikes" #simple DB name - not built for security
    USER = "dublinbikes" # simple user name - not built for security
    PASSWORD="dublinbikes" #simple password - not built for security

    engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
    return engine

def setupTables():
    #creates database table - station
    sql = """
    CREATE TABLE IF NOT EXISTS station (
    number INTEGER,
    name VARCHAR(256),
    position_lat REAL,
    position_lng REAL,
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
    status VARCHAR(256),
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
    lat REAL,
    lng REAL,
    temp REAL,
    temp_max REAL,
    temp_min REAL,
    pressure INTEGER,
    windspeed INTEGER,
    humidity REAL,
    conditions VARCHAR(256),
    time INTEGER
    )
    """
    try:
        res = engine.execute("DROP TABLE IF EXISTS weather")
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)#, traceback.format_exc())

def dbWrite(engine,station,weather):
    
    #inserts static station data values to DB (really this only needs to be done once..... inefficient to do it each time as data doesnt change!
    sql = "INSERT INTO station VALUES (" + str(station['stationNumber']) +", '" + str(station['stationName']) + "'," + str(station['stationLat']) + "," + str(station['stationLong']) + "," + str(station['stationBikeStands']) + ");"
    
    try:
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

    #inserts dynamic station data values to DB - note need to reformat time variable as too large for database...
    sql = "INSERT INTO availability VALUES (" + str(station['stationNumber']) +", '" + str(station['stationStatus']) + "'," + str(station['stationAvailableBikes']) + "," + str(station['stationAvailableStands']) + "," + str(station['lastUpdate']) + ");"
    
    try:
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

    #inserts weather  data values to DB - note need to reformat time variable as too large for database...
    sql = "INSERT INTO weather VALUES (" + str(weather['lat']) +", " + str(weather['long']) +", " + str(weather['temp']) +", " + str( weather['temp_max']) +", " + str(weather['temp_min']) +", " + str(weather['pressure']) +", " + str(weather['humidity']) +", "+ str(weather['wind']) +", '" + str(weather['sky']) +"', " + str( weather['dt']) + ");"
    
    try:
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)



#some test statements
        
##station = {'stationAvailableBikes': 0, 'stationLong': -6.262287, 'stationStatus': 'OPEN', 'stationLat': 53.340962, 'lastUpdate': 1490816007000, 'stationBikeStands': 29, 'stationName': 'CHATHAM STREET', 'stationAvailableStands': 29, 'stationNumber': 1}
##weather = {'long': -6.26, 'humidity': 82, 'sky': 'Rain', 'temp_min': 12, 'temp': 12.49, 'lat': 53.34, 'dt': 1490814000, 'city': 'Dublin', 'temp_max': 13, 'pressure': 1011, 'wind': 5.1}
##print(str(station['stationNumber']), station['stationName'], station['stationLat'], station['stationLong'], station['stationBikeStands']) # static bike info
##print(station['stationNumber'],station['stationStatus'], station['stationAvailableBikes'], station['stationAvailableStands'], station['lastUpdate']) # dynamic bike info
##print(str(1), weather['city'],weather['lat'], weather['long'],weather['temp'], weather['temp_max'], weather['temp_min'], weather['pressure'],  weather['wind'], weather['sky'], weather['dt'] ) # weather info

##engine=accessDB()
##
##accessDB()
##setupTables()
##dbWrite(engine,station,weather)
