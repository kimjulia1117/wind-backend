import os
import urllib
import json
import datetime
import requests

#Future reference: Assuming that data is successfully stored into database,
#we should not have to worry about keeping the data in these files and replace
#the information with the new data.

#TODO: Need to get data live time
#Grab data from current directory up until after 6 hours
#If 6 hours passed, then check to see if the new folder is up
#If not, use the next hour in the current directory, check if new directory is up
#Do this if the directory is not up 
#Once the folder is up, get the equivalent timestamp for the new directory to get updated predictions

current_datetime = datetime.datetime.utcnow()
noaa = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl'
latLon = '&leftlon=0&rightlon=360&toplat=90&bottomlat=-90'
#date format: <year><month><day>
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
#hour can be 00, 06, 12, or 18
refHour = (current_datetime.hour / 6) * 6
#recorded_hour ranges from 000 to 384 (0 to 16 days, every 3 hours)
recorded_hour = (current_datetime.hour / 3) * 3
#file name format: gfs.t<hour>z.pgrb2.1p00.f<recorded_hour>
fileName = 'gfs.t' + "{:02d}".format(refHour) + 'z.pgrb2.1p00.f' + "{:03d}".format(recorded_hour)

url = noaa + '?file=' + fileName + latLon + '&dir=%2Fgfs.' + str(year) + "{:02d}".format(month) + "{:02d}".format(day) + '%2F' + "{:02d}".format(refHour)
urllib.urlretrieve(url, './data/data.grb2')

print('Retrieve data from NOAA: SUCESS!')

goToGrib2JSON = 'grib2json/target/grib2json-0.8.0-SNAPSHOT/bin'
os.chdir(goToGrib2JSON)

#** will need to group the U and V data together by time or name of file **
#(--fp) parameterNumber: 2 (U-component_of_wind)
#				         3 (V-component_of_wind)
#(--fs) Height level above ground => surface1Type: 103
#(--fv) surface1Value: 10.0

#Note: If data failed to convert, maybe have it go into an ongoing loop
#for every 10 seconds (more or less) or keep going with the future incoming data?

convertForUComponent = 'sh grib2json --names --data --fp 2 --fs 103 --fv 10.0 --output ../../../../data/u_comp.json ../../../../data/data.grb2'
os.system(convertForUComponent)

convertForVComponent = 'sh grib2json --names --data --fp 3 --fs 103 --fv 10.0 --output ../../../../data/v_comp.json ../../../../data/data.grb2'
os.system(convertForVComponent)

print('Converting from grib2 to json: SUCCESS!')

goToData = '../../../../data'
os.chdir(goToData)

if recorded_hour >= 24:
    addDay = recorded_hour / 24
    recorded_hour = recorded_hour % 60
else:
    addDay = 0

if addDay != 0: 
    day = day + addDay

with open("u_comp.json") as fo:
    data1 = json.load(fo)

data1[0]['recordedTime'] = str(year) + '-' + "{:02d}".format(month) + '-' + "{:02d}".format(day) + ' ' + "{:02d}".format(recorded_hour) + ':00:00+00'
with open("u_comp.json", "w") as fo:
    json.dump(data1, fo)

with open("v_comp.json") as fo:
    data2 = json.load(fo)

data2[0]['recordedTime'] = str(year) + '-' + "{:02d}".format(month) + '-' + "{:02d}".format(day) + ' ' + "{:02d}".format(recorded_hour) + ':00:00+00'
with open("v_comp.json", "w") as fo:
    json.dump(data2, fo)

data1.append(data2[0])

with open("wind_data.json", "w") as fo:
    json.dump(data1, fo)

print('Storing data onto files: SUCCESS!')

API_ENDPOINT = "http://localhost:3000/data"
r = requests.post(url = API_ENDPOINT)

print(r.text)
