import os
import urllib
import json

#Future reference: Assuming that data is successfully stored into database,
#we should not have to worry about keeping the data in these files and replace
#the information with the new data.

#TODO: Need to get data live time
url = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl?file=gfs.t06z.pgrb2.1p00.f006&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.20190902%2F06'
urllib.urlretrieve(url, './data/data.grb2')

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

with open("u_comp.json") as fo:
    data1 = json.load(fo)

with open("v_comp.json") as fo:
    data2 = json.load(fo)

data1.append(data2[0])

with open("wind_data.json", "w") as fo:
    json.dump(data1, fo)