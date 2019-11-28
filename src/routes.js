const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const connection = mysql.createPool({
    host: 'info-430-au19.database.windows.net',
    user: 'simkota',
    password: 'h3ll0fr!3nd$',
    database: 'yelpdata'
});

const app = express();

app.get('/resData', function (req, res) {
    connection.getConnection(function (err, connection) {
        connection.query('SELECT * FROM resData', (error, results, fields) => {
            if (error) throw error;

            res.send(results)
        });
    });
});

app.listen(3000, () => {
    console.log('Go to http://localhost:3000/resData')
});