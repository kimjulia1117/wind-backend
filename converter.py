import os
import urllib
import json

#Future reference: Assuming that data is successfully stored into database,
#we should not have to worry about keeping the data in these files and replace
#the information with the new data.

#TODO: Need to get data live time
noaa = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl'
latLon = '&leftlon=0&rightlon=360&toplat=90&bottomlat=-90'
#date format: <year><month><day>
year = 2019
month = 9
day = 12
#hour can be 00, 06, 12, or 18
hour = 0
#minute ranges from 000 to 384 (0 to 6.4 hours)
minute = 360
#file name format: gfs.t<hour>z.pgrb2.1p00.f<minute>
fileName = 'gfs.t' + "{:02d}".format(hour) + 'z.pgrb2.1p00.f' + "{:03d}".format(minute)

url = noaa + '?file=' + fileName + latLon + '&dir=%2Fgfs.' + str(year) + "{:02d}".format(month) + "{:02d}".format(day) + '%2F' + "{:02d}".format(hour)
urllib.urlretrieve(url, './data/data.grb2')

print('Success!')

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

goToData = '../../../../data'
os.chdir(goToData)

if minute >= 60:
    addHours = minute / 60
    minute = minute % 60
else:
    addHours = 0

if addHours != 0: 
    hour = hour + addHours

with open("u_comp.json") as fo:
    data1 = json.load(fo)

data1[0]['recordedTime'] = str(year) + '-' + "{:02d}".format(month) + '-' + "{:02d}".format(day) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':00+00'
with open("u_comp.json", "w") as fo:
    json.dump(data1, fo)

with open("v_comp.json") as fo:
    data2 = json.load(fo)

data2[0]['recordedTime'] = str(year) + '-' + "{:02d}".format(month) + '-' + "{:02d}".format(day) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':00+00'
with open("v_comp.json", "w") as fo:
    json.dump(data2, fo)

data1.append(data2[0])

with open("wind_data.json", "w") as fo:
    json.dump(data1, fo)