from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map, icons
import json
import requests

app = Flask(__name__)

#set your googlemaps api key
app.config['GOOGLEMAPS_KEY']="AIzaSyB4ipnj_JcaXKHFruw172nwitgJWdcV9Fk" #Daniel McMahon's Key
#initalize the extension
GoogleMaps(app)


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
            r = requests.get("https://api.jcdecaux.com/vls/v1/stations/" + str(i) + "?contract=Dublin&apiKey=c64916b14c557faa49fdf72b8902e4d9ff9afe35")
            data = r.json()
            
            #note: using value of bike station numbers as value of each button...
            infobox = "Name: " + str(data["name"]) + "<br/>" + "Status: " + str(data["status"]) + "<br/>" + "Available Stands: " + str(data["available_bike_stands"]) + "</br>" + "Available Bikes: " + str(data["available_bikes"]) + "</br>" + "Historic Info: " + '<input type="submit" name="' + str(data["number"]) + '" value="See More" onclick="showDiv(' + "'" + str(data["name"]) + "'" +')">'
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

    return render_template('index.html', trdmap=trdmap)



#def main():
#  return render_template("index.html")

if __name__ == "__main__":
  app.run()
