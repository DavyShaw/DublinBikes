import requests
import json
import time

while(True):
        #using time variables for our filenames to make them distinct - will help with database setup
        minutes = str(time.gmtime().tm_min)
        hour = str(time.gmtime().tm_hour)
        day =  str(time.gmtime().tm_mday)
        month =  str(time.gmtime().tm_mon)
        year = str(time.gmtime().tm_year)

        #check of current processing filename
        print("Station-Data-" + hour + "-" + minutes + "-" + day + "-" + month + "-" + year)

        #creates or resets existing file due to write permissions - allows us to make overall array to store data
        with open("Station-Data-" + hour + "-" + minutes + "-" + day + "-" + month + "-" + year + ".json", "w") as file:
                file.write("[")

        #note we're also throwing in the station number that doesn't exist (station 50) so it's easier to get hold of
        #data by array number later - keeps the offset of array values by 1
        for i in range(1,103):
                #basic json request to get live data at each station from 1 up to 102
                r = requests.get("https://api.jcdecaux.com/vls/v1/stations/" + str(i) + "?contract=Dublin&apiKey=c64916b14c557faa49fdf72b8902e4d9ff9afe35")
                data = r.json()
                #mimic counter to ensure script hasn't crashed goes to 102%
                #print(i, "%") 

                #writes json value to file also includes comma after each value to segment the data from the next installment
                #note this results in an extra comment at end of data but does not appear to cause error
                with open("Station-Data-" + hour + "-" + minutes + "-" + day + "-" + month + "-" + year + ".json","a") as file:
                    json.dump(data, file, ensure_ascii=False)
                    file.write(",")

        #stops array at end of file by inserting square bracket
        with open("testOverallData.json","a") as file:
                file.write("]")
        time.sleep(900) #15 minute sleep
