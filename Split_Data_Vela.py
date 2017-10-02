import requests
import numpy as np
import datetime
import csv

directory = 'Vela_Pulsar/'
file = open(directory + 'elevation_vela.txt', 'r')
text = file.read()
textSplit = text.split('\n')
dateTime = []
date_Time = []
month = []
day = []
year = []
hour = []
minute = []
second = []
elevationAngle = []
theta = []
altitude = []
longitude = []
latitude = []

for i in range(len(textSplit)):
    textSplit[i] = textSplit[i].split('\t')
    dateTime.append(textSplit[i][0])
    dateTime[i] = dateTime[i].split('-')
    dateTime[i][0] = dateTime[i][0].split('/')
    dateTime[i][1] = dateTime[i][1].split(':')
    month.append(float(dateTime[i][0][1]))
    day.append(float(dateTime[i][0][2]))
    year.append(float(dateTime[i][0][0]))
    hour.append(float(dateTime[i][1][0]))
    minute.append(float(dateTime[i][1][1]))
    second.append(float(dateTime[i][1][2]))
    hour[i] = hour[i] + minute[i]/60 + second[i]/3600
    elevationAngle.append(float(textSplit[i][1]))
    altitude.append(float(textSplit[i][2])/1000)
    longitude.append(float(textSplit[i][3]))
    latitude.append(float(textSplit[i][4]))

with open(directory + "month.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(month)
with open(directory + "day.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(day)
with open(directory + "year.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(year)
with open(directory + "hour.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(hour)
with open(directory + "elevationAngle.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(elevationAngle)
# with open(directory + "theta.csv", "w") as output:
#     wr = csv.writer(output, quoting=csv.QUOTE_ALL)
#     wr.writerow(theta)
with open(directory + "altitude.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(altitude)
with open(directory + "longitude.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(longitude)
with open(directory + "latitude.csv", "w") as output:
    wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    wr.writerow(latitude)
