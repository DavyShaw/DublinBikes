#script cross checked the static Dublin.json file to compare station numbers
#highlights missing station numbers 0 + 50

import json

stations=[]
nonExist=[]

with open("Dublin.json","r") as data_file:
    data = json.load(data_file)

for i in range(0,101):
    stations.append(data[i]["number"])

stations.sort()
print("The following are valid station numbers:")
print(stations)
print()

#this checks if any numbers 0-102 aren't valid stations
for i in range(0,102):
    if i not in stations:
        nonExist.append(i)

nonExist.sort()
print("The following are not valid station numbers:")
print(nonExist)
