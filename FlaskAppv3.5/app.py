from flask import Flask, g, render_template, jsonify
from flask_googlemaps import GoogleMaps, Map, icons
from sqlalchemy import create_engine
import config
import json
import requests

app = Flask(__name__)

#set your googlemaps api key
app.config['GOOGLEMAPS_KEY']="AIzaSyB4ipnj_JcaXKHFruw172nwitgJWdcV9Fk" #Daniel McMahon's Key
#initalize the extension
GoogleMaps(app)

def connect_to_database():
    db_str = "mysql+mysqldb://{}:{}@{}:{}/{}"
    engine = create_engine(db_str.format(config.USER,
                                        config.PASSWORD,
                                        config.URI,
                                        config.PORT,
                                        config.DB),
                           echo=True)

    return engine

def get_db():
    '''function sets up database connection'''
    engine = getattr(g, 'engine', None)
    if engine is None:
        engine = g.engine = connect_to_database()
    return engine

##def station(station_id):
##    '''this function sends SQL query to database based on station_id number passed in.. Returns JSON'''
##    
##    sql = """
##    SELECT available_bikes, available_bike_stands,last_update from stationDynamic where number = {}
##    """.format(station_id)
##    
##    engine = get_db()
##    rows = engine.execute(sql).fetchall()  # we use fetchall(), but probably there is only one station
##    res = [dict(row.items()) for row in rows]  # use this formula to turn the rows into a list of dicts
##    #data = jsonify(data=res)  # jsonify turns the objects into the correct respose
##    #print(data)
##    #return data.get_data(as_text=True) #returns as string?
##    jdata = json.dumps(res)
##    #engine.dispose() #may not be right..... should close connection
##    return jdata

@app.route("/")
def mapview():
    '''code adapted from http://flaskgooglemaps.pythonanywhere.com/
    http://stackoverflow.com/questions/32201678/how-to-get-json-data-from-a-url-using-flask-in-python'''
    
    #with open('./static/Dublin.json') as data_file:
	#data = json.load(data_file)           
    output = []    
    
    #note there is no station 50 so need to split the ranges
    for i in range(1,103):
        if(i!=50):
            #backup dublinbikes key (stephens: 88e5dc7b2582c68724462d2d858361ca93582780)
            #main dublinbikes key(daniels: c64916b14c557faa49fdf72b8902e4d9ff9afe35)
            r = requests.get("https://api.jcdecaux.com/vls/v1/stations/" + str(i) + "?contract=Dublin&apiKey=88e5dc7b2582c68724462d2d858361ca93582780")
            data = r.json()
            
            #note: using value of bike station numbers as value of each button...
            infobox = "Name: " + str(data["name"]) + "<br/>" + "Status: " + str(data["status"]) + "<br/>" + "Available Stands: " + str(data["available_bike_stands"]) + "</br>" +  "Available Bikes: " + str(data["available_bikes"]) + "</br>" + "Historic Info: " + '<input type="submit" name="' + str(data["number"]) + '" value="See More" onclick="showDiv(' + "'" + str(data["name"]) + "'" + "," + "'" +  str(data["number"]) + "'" + ')">'
            
            output.append(
                    {
                            'icon': icons.dots.blue,
                            'lat': data["position"]["lat"],
                            'lng': data["position"]["lng"],
                            'infobox': infobox
                    }
                )

        trdmap = Map(
            identifier="trdmap",
            lat=53.350140,
            lng=-6.266155,

	#potential extra feature - needs custom styling however...
	#see http://flaskgooglemaps.pythonanywhere.com/ clusterd map in view
	#cluster=True,
	#cluster_gridsize=10,

	#note: style for map is being declared here...
            style="height:600px;width:800px;margin-left:50px;margin-right:50px;color:black;float:left;display:inline-block;box-shadow: 10px 10px 5px #888888",
               
            markers = output
    )

    station(data["number"])

    return render_template('index.html', trdmap=trdmap)


@app.route('/station/<int:station_id>')
def station(station_id):
    sql = """
    SELECT available_bikes, available_bike_stands,last_update from stationDynamic where number = {}
    """.format(station_id)
    
    engine = get_db()
    rows = engine.execute(sql).fetchall()  # we use fetchall(), but probably there is only one station
    res = [dict(row.items()) for row in rows]  # use this formula to turn the rows into a list of dicts
    data = jsonify(data=res)  # jsonify turns the objects into the correct respose
    #print(data)
    return data #.get_data(as_text=True) #returns as string?

if __name__ == "__main__":
  app.run()
