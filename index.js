const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const port = 3000
const db = require('./queries')

app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
        extended: true,
    })
)
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get('/', (request, response) => {
    response.json({info: 'Node.js, Express, and Postgres API' })
})

app.get('/health', (request, response) => {
    response.json({message: 'GET HEALTH STATUS : OK !'})
})

app.get('/data', db.getAllDataFromDatabase)
app.post('/data', db.postDataFromSource)
app.put('/data', db.updateData)
app.get('/data/latest', db.getLatestDataFromDatabase)
app.get('/data/:recorded_time', db.getDataByRecordedTime)
app.delete('/data/old', db.flushOldData)
app.delete('/data/all', db.flushAll)

app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})