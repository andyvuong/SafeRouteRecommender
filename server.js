var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');

var app = express();

// Configs
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());


// router
var router = require('./router')(app);

module.exports = app;
app.listen(8000);
console.log("Listening on port 8000");
