import requests
import urllib
import json
import time


def bikesApiCall(stationnum):
        api_key = "c64916b14c557faa49fdf72b8902e4d9ff9afe35"
        r = requests.get("https://api.jcdecaux.com/vls/v1/stations/" + str(stationnum) + "?contract=Dublin&apiKey=" + api_key)
        data = r.json()
        return data

def  organisedBikeData(data):
        dictionaryData = dict(
                stationNumber=  data.get('number'),
                stationName= data.get('name'),
                stationLat= data.get('position').get('lat'),
                stationLong= data.get('position').get('lng'),
                stationStatus=  data.get('status'),
                stationAvailableStands=  data.get('available_bike_stands'),
                stationAvailableBikes=  data.get('available_bikes')
        )
        return dictionaryData

def latValues(data):
        stationLat= data.get('position').get('lat')
        return stationLat

def longValues(data):
        stationLong= data.get('position').get('lng')
        return stationLong

def weatherApiCall(lat,long): #Part of code taken from: https://straymarcs.net/2014/12/how-to-create-your-own-weather-forecast-program-using-python/
    api_key = '44b78ac274e9d94337e6620489fdcdbe' #Davy's Open Weather Map API Ky
    unit = 'metric'
    api = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(long) #St James Hospital #Replace the values of the altitude and longitude to accept other locations
    api_url = api + '&mode=json&units=' + unit + '&APPID=' + api_key
    return api_url

def weatherRequest(api_url): #http://codereview.stackexchange.com/questions/131371/script-to-print-weather-report-from-openweathermap-api
    url = urllib.request.urlopen(api_url)
    output = url.read().decode('utf-8')
    api_data = json.loads(output)
    url.close()
    return api_data

def organisedWeatherData(api_data):
    data = dict(
        city=api_data.get('name'),
        country=api_data.get('sys').get('country'),
        temp=api_data.get('main').get('temp'),
        temp_max=api_data.get('main').get('temp_max'),
        temp_min=api_data.get('main').get('temp_min'),
        humidity=api_data.get('main').get('humidity'),
        pressure=api_data.get('main').get('pressure'),
        sky=api_data['weather'][0]['main'], #clouds?
        dt=api_data.get('dt') #daytime in weird format
    )
    return data

for i in range(1,103):
        if i!=50:
                print(organisedBikeData(bikesApiCall(i)))
                print(organisedWeatherData(weatherRequest(weatherApiCall(latValues(bikesApiCall(i)), longValues(bikesApiCall(i))))))
                

##      counter = 0
##
##        
##        #timed to execute for total of 7 days (10,080 minutes @ 5mins per scrape)
##        while(counter<2016):
##                
##                #using time variables for our filenames to make them distinct - will help with database setup
##                minutes = str(time.gmtime().tm_min)
##                hour = str(time.gmtime().tm_hour)
##                day =  str(time.gmtime().tm_mday)
##                month =  str(time.gmtime().tm_mon)
##                year = str(time.gmtime().tm_year)
##
##                #check of current processing filename
##                print("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes)
##
##                #creates or resets existing file due to write permissions - allows us to make overall array to store data
##                with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes +".json", "w") as file:
##                        file.write("[")
##
##                #note we're also throwing in the station number that doesn't exist (station 50) so it's easier to get hold of
##                #data by array number later - keeps the offset of array values by 1
##                for i in range(1,103):
##                        
##                        #basic json request to get live data at each station from 1 up to 102
##                        r = requests.get("https://api.jcdecaux.com/vls/v1/stations/" + str(i) + "?contract=Dublin&apiKey=c64916b14c557faa49fdf72b8902e4d9ff9afe35")
##                        data = r.json()
##                        #mimic counter to ensure script hasn't crashed goes to 102%
##                        #print(i, "%")
##
##                        #get hold of latitude/longitude coordinates for current station (adapted for Davy's OpenWeatherMap code):
##                        latitude = data.get('position').get('lat')
##                        longitude = data.get('position').get('lng')
##                        print(latitude,longitude)
##
##                        lat
##                     
##                        #writes json value to file also includes comma after each value to segment the data from the next installment
##                        #note this results in an extra comment at end of data but does not appear to cause error
##                        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes+ ".json","a") as file:
##                            json.dump(data, file, ensure_ascii=False)
##                            file.write(",")
##                        
##                #stops array at end of file by inserting square bracket
##                with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes +".json","a") as file:
##                        file.write("]")
##                        
##                #increase counter by 1 each time
##                counter+=1
##                        
##                #5 minute sleep
##                time.sleep(300) 

