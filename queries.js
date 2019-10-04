const Pool = require('pg').Pool
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'postgres',
    password: 'v9BbsE7wLaF9Nw9A',
    port: 5432,
})

/* Table format:
 *  wind_data (
        recorded_time timestamp with time zone,
        header jsonb,
        data decimal[]
    );
 * 
 * Get all data from the PostgreSQL database
 */
const getAllDataFromDatabase = (request, response) => {
    pool.query('SELECT * FROM wind_data;', (error, results) => {
        if (error) {
            response.status(404).json({message: error}); 
            throw error;
        }
        response.status(200).json({count: results.rows.length, results: results.rows});
    });
}

/*
 * Get the latest available data from the PostgreSQL database
 */
const getLatestDataFromDatabase = (request, response) => {
    pool.query("SELECT * FROM wind_data WHERE recorded_time = (SELECT MAX(recorded_time) FROM wind_data)", (error, results) => {
        if (error) {
            response.status(404).json({message: error});
            throw error;
        }
        response.status(200).json(results.rows);
    });
}

const getDataByDateTime = (request, response) => {
    const datetime = request.params.datetime
    pool.query("SELECT * FROM wind_data WHERE recorded_time = $1", [datetime], (error, results) => {
        if (error) {
            throw error
        }
        response.status(200).json(results.rows)
    })
}
/*
 * Get data from online source and store into PostgreSQL database
 */
const postDataFromSource = (request, response) => {
    var fs = require("fs");
    var content = String(fs.readFileSync("./data/wind_data.json"));

    parseFile = JSON.parse(content);

    for(var i = 0; i < parseFile.length; i++) {
        header = parseFile[i]["header"];
        dataArray = parseFile[i]["data"];
        recordedTime = parseFile[i]["recordedTime"];

        pool.query("INSERT INTO wind_data VALUES ($1, $2, $3)", [recordedTime, header, dataArray], (error, results) => {
            if (error) {
                response.status(404).json({message: error}); 
                throw error;
            }

        });
    }
    response.status(200).json("POST DATA FROM SOURCE STATUS : OK !");
}

/*
 * To open up space, delete week old data from the PostgreSQL database
 */
const flushOldData = (request, response) => {
    pool.query("SELECT * FROM wind_data"), (error, results) => {
        if (error) {
            response.status(404).json({message: error}); 
            throw error;
        }
    }
    //TODO: Determine when recorded_time is a week old or older, then delete
    response.status(200).json("FLUSH OLD DATA: OK !");
}

/*
 * Used only for testing purposes
 */
const flushAll = (request, response) => {
    pool.query("TRUNCATE wind_data;", (error, results) => {
        if (error) {
            response.status(404).json({message: error}); 
            throw error;
        }
        response.status(200).json(results.rows)
    });
}


module.exports = {
    getAllDataFromDatabase,
    getLatestDataFromDatabase,
    getDataByDateTime,
    postDataFromSource,
    flushOldData,
    flushAll
}