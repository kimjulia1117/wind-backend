# wind-backend
<img src="https://github.com/kimjulia1117/wind-backend/blob/master/icons/express-icon.png" height="50" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/kimjulia1117/wind-backend/blob/master/icons/node-js-icon.png" height="100" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/kimjulia1117/wind-backend/blob/master/icons/postgresql-icon.png" height="100" />

Run API:
```node index.js```

Run converter:
```python ./converter.py```

***Before running converter.py, need to download grib2json***

Used Grib2JSON to help convert data from grib2 to JSON: https://github.com/cambecc/grib2json

Data from NOAA: https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl

Helpful links:
- https://blog.logrocket.com/setting-up-a-restful-api-with-node-js-and-postgresql-d96d6fc892d8/
- https://github.com/newsdev/simple-wind
- https://github.com/danwild/wind-js-server

# How to set it up
1. Download PostgreSQL. After downloading the whole package, there is a SQL Shell that you can use (psql). There, you put in the information to get into the database, which is what is going on in the beginning of the queries.js file.

2. Replace the empty grib2json file with the grib2json repo (https://github.com/cambecc/grib2json).

3. Go into the grib2json directory and type ```mvn package``` (you may need to install the mvn command)

4. Go into the target directory within the grib2json directory. There should be a “grib2json-0.8.0-SNAPSHOT.tar.gz” file. Gunzip/tar the file.
- NOTE: The grib2json file uses $JAVA_HOME so make sure you have that set up to wherever your Java is installed in.

5. Make sure that you have these 2 crontabs:
- For MacOS, I used the command “crontab -e” to insert in my crontabs to run the converter.py and the deleteOld.py scripts
- For testing purposes, I have it running every 5 minutes (does NOT mean it is getting live time data in 5 minute intervals, it just means that it is attempting to get the latest data available every 5 minutes in case if one of the previous times the script tries to run fails for whatever reason)
- For example:
```*/5 * * * * python ~/projects/wind-backend/converter.py```
```*/5 * * * * python ~/projects/wind-backend/deleteOld.py```

6. Run the API by doing ```node index.js```

7. The API uses port 3000. To see the list of routes, refer to routes.js.
