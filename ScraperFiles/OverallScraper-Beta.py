import requests
import urllib
import json
import time

#importing elements from other python file
from MySQLBasicDBSetup import accessDB as engine
from MySQLBasicDBSetup import setupTables as tables
#from MySQLBasicDBSetup import dbWrite

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
                stationAvailableBikes=  data.get('available_bikes'),
                lastUpdate= data.get('last_update')
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

def  fileBackupBikes(data):
        #using time variables for our filenames to make them distinct - will help with database setup
        minutes = str(time.gmtime().tm_min)
        hour = str(time.gmtime().tm_hour)
        day =  str(time.gmtime().tm_mday)
        month =  str(time.gmtime().tm_mon)
        year = str(time.gmtime().tm_year)
                
        #creates or resets existing file due to write permissions - allows us to make overall array to store data
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes +".json", "w") as file:
                file.write("[")

        #writes json value to file also includes comma after each value to segment the data from the next installment
        #note this results in an extra comment at end of data but does not appear to cause error
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes+ ".json","a") as file:
                json.dump(data, file, ensure_ascii=False)
                file.write(",")
                        
        #stops array at end of file by inserting square bracket
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes +".json","a") as file:
                file.write("]")

        print("Bike Data Successfully Backed Up!")

def  fileBackupWeather(data):
        #using time variables for our filenames to make them distinct - will help with database setup
        minutes = str(time.gmtime().tm_min)
        hour = str(time.gmtime().tm_hour)
        day =  str(time.gmtime().tm_mday)
        month =  str(time.gmtime().tm_mon)
        year = str(time.gmtime().tm_year)
                
        #creates or resets existing file due to write permissions - allows us to make overall array to store data
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Weather-Data-" + hour + "-" + minutes +".json", "w") as file:
                file.write("[")

        #writes json value to file also includes comma after each value to segment the data from the next installment
        #note this results in an extra comment at end of data but does not appear to cause error
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Weather-Data-" + hour + "-" + minutes+ ".json","a") as file:
                json.dump(data, file, ensure_ascii=False)
                file.write(",")
                        
        #stops array at end of file by inserting square bracket
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Weather-Data-" + hour + "-" + minutes +".json","a") as file:
                file.write("]")

        print("Weather Data Successfully Backed Up!")


if __name__ == "__main__":
        # logs into DB
        engine
        
        # WARNING - RESETS TABLES - DO NOT RUN WHILE SCRIPT IS ACTIVE ON EC2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        tables
        
        #initialising counter for scraper
        counter = 0
        
        #timed to execute for total of 7 days (10,080 minutes @ 5mins per scrape)
        while(counter<2016):
                
                #access data
                for i in range(1,103):
                        if i!=50:

                                #using variables for easier readability
                                bikeJson = bikesApiCall(i)
                                weatherJson = weatherRequest(weatherApiCall(latValues(bikesApiCall(i)), longValues(bikesApiCall(i))))
                                                             
                                #writes jsondata to file as backup in event some weird error occurs
                                #not quite right - this rewrites the file each time i is rechecked...
                                #fileBackupBikes(bikeJson)
                                #fileBackupWeather(weatherJson)
                                
                                #current station and weather dictionary data
                                station = organisedBikeData(bikeJson)
                                weather = organisedWeatherData(weatherJson)

                                #writes data to database            
                                #dbWrite(station,weather)

                                #Mimic counter to ensure script hasnt crashed - runs to 102%
                                print(i, "%")
                        
        #increment our counter in while loop - sentinel value
        counter += 1
        #5 minute sleep
        time.sleep(300)


                
                
                



