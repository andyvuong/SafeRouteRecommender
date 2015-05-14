var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var path = require("path");
var PythonShell = require("python-shell");
var app = express();

// Configs
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());

app.use('/', express.static('public'));

// router
var router = require('./router')(app);


module.exports = app;
app.listen(process.env.PORT || 3000);
console.log("Safe Route Recommender");
console.log("Listening on port 3000");
