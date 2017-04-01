import requests
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import time
import datetime

#importing elements from other python file
from MySQLBasicDBSetup import dbWrite

def bikesApiCall(stationnum):
        api_key = "c64916b14c557faa49fdf72b8902e4d9ff9afe35"
        url = urllib.request.Request("https://api.jcdecaux.com/vls/v1/stations/" + str(stationnum) + "?contract=Dublin&apiKey=" + api_key)
        try:
                urllib.request.urlopen(url)
        except HTTPError as e:
                #if http error were going to return an ERROR string
                data = "ERROR"
                #if server error were going to return an ERROR string
        except URLError as e:
                data = "ERROR"
        else:
                url = urllib.request.urlopen(url)
                output = url.read().decode('utf-8')
                data = json.loads(output)
                url.close()
        return data

def  organisedBikeData(data):
        
        #note: code translates time since epoch (milliseconds)
        #ec2 instance app runs on does not have correct time set due to daylight savings
        #adding an hour in seconds to epoch time
        
        daylightsavings= 3600000
        y = int(data.get('last_update') + daylightsavings)
        x = time.gmtime(y/1000)
        timeUpdate = str(time.strftime('%d-%m-%Y-%H:%M:%S', x))
        
        dictionaryData = dict(
                stationNumber=  data.get('number'),
                stationName= data.get('name'),
                stationLat= data.get('position').get('lat'),
                stationLong= data.get('position').get('lng'),
                stationStatus=  data.get('status'),
                stationBikeStands=  data.get('bike_stands'),
                stationAvailableStands=  data.get('available_bike_stands'),
                stationAvailableBikes=  data.get('available_bikes'),
                lastUpdate= timeUpdate
        )
        return dictionaryData

def  fileBackupBikes(data,minute,hour,day,month,year):
        
        #writes json value to file also includes comma after each value to segment the data from the next installment
        #note this results in an extra comment at end of data but does not appear to cause error
        with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes+ ".json","a") as file:
                json.dump(data, file, ensure_ascii=False)
                file.write(",")

        #print("Bike Data Successfully Backed Up!"))

if __name__ == "__main__":

        #initialising counter for scraper
        counter = 0
        
        #timed to execute for total of 7 days (10,080 minutes @ 5mins per scrape)
        while(counter<2016):

                #filename variables
                minutes = str(time.gmtime().tm_min)
                hour = str(time.gmtime().tm_hour)
                day =  str(time.gmtime().tm_mday)
                month =  str(time.gmtime().tm_mon)
                year = str(time.gmtime().tm_year)

                #creates or resets existing file due to write permissions - allows us to make overall array to store json data
                with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes +".json", "w") as file:
                        file.write("[")
                
                #access data
                for i in range(1,103):
                        if i!=50:

                                #using variables for easier readability
                                bikeJson = bikesApiCall(i)

                                #if our weather or bike json calls return an error then we are going to skip this round and move on...
                                if bikeJson != "ERROR":
                                        
                                        #writes jsondata to file as backup in event some weird error occurs
                                        #not quite right - this rewrites the file each time i is rechecked...
                                        fileBackupBikes(bikeJson,minutes,hour,day,month,year)
                                        
                                        #current station and weather dictionary data
                                        station = organisedBikeData(bikeJson)
                                      
                                        #writes data to database
                                        dbWrite(station)

                                #Mimic counter to ensure script hasnt crashed during a processed run - runs to 102%
                                print(i, "%")

                #stops array at end of file by inserting square bracket
                with open("FileNum-" + str(counter) + "-" + day + "-" + month + "-" + year  + "-Station-Data-" + hour + "-" + minutes +".json","a") as file:
                        file.write("]")
                
                #increment our counter in while loop - sentinel value
                #note this is approximate as the scraping takes a couple minutes each turn
                #most likely a manual close of the script will be needed however this is a built in cut off
                #in the event the code is forgotten to be manually switched off it will terimate after 2016 loops
                counter += 1

                print("Finished loop: " + str(counter) + "/2016")
                
                #5 minute sleep
                time.sleep(300)


                
                
                



