import os
import urllib2
import json
import datetime
import requests
import sys

#Future reference: Assuming that data is successfully stored into database,
#we should not have to worry about keeping the data in these files and replace
#the information with the new data.

#Grab data from current directory up until after 6 hours
#If 6 hours passed, then check to see if the new folder is up
#If not, use the next hour in the current directory, check if new directory is up
#Do this if the directory is not up 
#Once the folder is up, get the equivalent timestamp for the new directory to get updated predictions

# out = os.popen('echo $JAVA_HOME').read()
# os.environ["JAVA_HOME"] = out
current_datetime = datetime.datetime.utcnow()
noaa = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl'
latLon = '&leftlon=0&rightlon=360&toplat=90&bottomlat=-90'
#date format: <year><month><day>
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
#refHour can be 00, 06, 12, or 18
refHour = ((current_datetime.hour / 6) * 6)
#recorded_hour ranges from 000 to 384 (0 to 16 days, every 3 hours)
recorded_hour = (current_datetime.hour / 3) * 3
fdir = os.path.abspath(os.path.dirname(__file__))

def convertData(year, month, day):
    goToGrib2JSON = './grib2json/target/grib2json-0.8.0-SNAPSHOT/bin'
    gribPath = os.path.join(fdir, goToGrib2JSON)
    os.chdir(gribPath)
    print("goToGrib2JSON path")

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

def getData(year, month, day, refHour):
    hourWithinRef = recorded_hour - refHour
    if hourWithinRef < 0:
        hourWithinRef = hourWithinRef * (-1)
    #file name format: gfs.t<hour>z.pgrb2.1p00.f<hourWithinRef>
    fileName = 'gfs.t' + "{:02d}".format(refHour) + 'z.pgrb2.1p00.f' + "{:03d}".format(hourWithinRef)
    print "Attempt to download: " + fileName
    url = noaa + '?file=' + fileName + latLon + '&dir=%2Fgfs.' + str(year) + "{:02d}".format(month) + "{:02d}".format(day) + '%2F' + "{:02d}".format(refHour)

    try:
        u = urllib2.urlopen(url)
    except urllib2.URLError, e:
        print e
        if refHour == 0:
            if month == 1 and day == 1:
                year = year - 1
                month = 12
                day = 31
                refHour = 18
                getData(year, month, day, refHour)
            elif (month == 5 or month == 7 or month == 8 or month == 10 or month == 12) and day == 1:
                month = month - 1
                day = 30
                refHour = 18
                getData(year, month, day, refHour)
            elif month == 3 and day == 1:
                if year % 4 == 0:
                    month = month - 1
                    day = 29
                    refHour = 18
                    getData(year, month, day, refHour)
                else:
                    month = month - 1
                    day = 28
                    refHour = 18
                    getData(year, month, day, refHour)
            elif (month == 2 or month == 4 or month == 6 or month == 9 or month == 11) and day == 1:
                month = month - 1
                day = 31
                refHour = 18
                getData(year, month, day, refHour)
            else:
                day = day - 1
                refHour = 18
                getData(year, month, day, refHour)
        else:    
            refHour = refHour - 6
            getData(year, month, day, refHour)
    else:
        datetimeFormat = str(year) + '-' + "{:02d}".format(month) + '-' + "{:02d}".format(day) + 'T' + "{:02d}".format(recorded_hour) + ':00:00.000Z'
        print datetimeFormat
        API_ENDPOINT = "http://localhost:3000/data/" + datetimeFormat
        r = requests.get(url = API_ENDPOINT)
        if r.text != "[]":
            print "Data already exists"
            sys.exit()
        local = './data/data.grb2'
        dataPath = os.path.join(fdir, local)
        f = open(dataPath, "w")
        content = u.read()
        f.write(content)
        f.close()
        print 'Downloading data: SUCCESS!'
        convertData(year, month, day)

getData(year, month, day, refHour)