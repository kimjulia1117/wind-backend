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
        ref_time timestamp,
        header jsonb,
        data decimal[]
    );
 * 
 * Get all data from the PostgreSQL database
 */
const getAllDataFromDatabase = (request, response) => {
    pool.query('SELECT * FROM wind_data;', (error, results) => {
        if (error) {
            response.status(404).json({message: error}) 
            throw error
        }
        response.status(200).json(results.rows)
    })
}

/*
 * Get the latest available data from the PostgreSQL database
 */
const getLatestDataFromDatabase = (request, response) => {
    pool.query("SELECT * FROM wind_data WHERE ref_time = (SELECT MAX(ref_time) FROM wind_data)", (error, results) => {
        if (error) {
            response.status(404).json({message: error});
            throw error;
        }
        response.status(200).json(results.rows);
    });
}

/*
 * Get data from online source and store into PostgreSQL database
 * TODO: Prevent duplicates from being stored into database
 */
const postDataFromSource = (request, response) => {
    var fs = require("fs");
    var content = String(fs.readFileSync("./data/wind_data.json"));

    parseFile = JSON.parse(content);

    for(var i = 0; i < parseFile.length; i++) {
        header = parseFile[i]["header"];
        dataArray = parseFile[i]["data"];
        refTime = header["refTime"];

        pool.query("INSERT INTO wind_data VALUES ($1, $2, $3)", [refTime, header, dataArray], (error, results) => {
            if (error) {
                response.status(404).json({message: error}); 
                throw error;
            }
        });
    }
    response.status(200).json("POST DATA FROM SOURCE STATUS : OK !");
}

/*
 * Detect when a new data and replace the current data
 */
const updateCurrentData = (request, response) => {

}

/*
 * To open up space, delete week old data from the PostgreSQL database
 */
const flushOldData = (request, response) => {
    pool.query()
}


module.exports = {
    getAllDataFromDatabase,
    getLatestDataFromDatabase,
    postDataFromSource,
    updateCurrentData,
    flushOldData
}