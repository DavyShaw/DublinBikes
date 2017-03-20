import requests
import time

#basic way to get data from website using requests library
response = requests.get("https://api.jcdecaux.com/vls/v1/stations/42?contract=Dublin&apiKey=c64916b14c557faa49fdf72b8902e4d9ff9afe35")
txt = response.text

#prints the response received from the link
print(txt)

#opens file and writes to it basic version
file = open("newfile.json","w")
file.write(txt)
file.close()

#creates 10 files reading json data every 60 seconds
while(True):
    for i in range(0,11):
        #need to make the requests again every few seconds - this is why its in loop
        response = requests.get("https://api.jcdecaux.com/vls/v1/stations/42?contract=Dublin&apiKey=c64916b14c557faa49fdf72b8902e4d9ff9afe35")
        txt = response.text
        #we use the i variable to get a different file name for each time data is read
        file = open("file_" + str(i) + ".json","w")
        file.write(txt)
        file.close()
        #cheaty way to get the loop to stop for 60 seconds....
        time.sleep(60)
