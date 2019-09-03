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

app.get('/', (request, response) => {
    response.json({info: 'Node.js, Express, and Postgres API' })
})

app.get('/health', (request, response) => {
    response.json({message: 'GET HEALTH STATUS : OK !'})
})

app.get('/data', db.getAllDataFromDatabase)
app.get('/post_data', db.postDataFromSource)
app.get('/latest', db.getLatestDataFromDatabase)

app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})