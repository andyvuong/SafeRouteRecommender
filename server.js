var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var path = require("path");
var PythonShell = require("python-shell");
var app = express();

/** Commented this out for now, we'll be using this later

var PythonShell = require('python-shell');
var options = {
    mode: 'text',
    scriptPath: '.',
    args: ['208 N. Harvey Urbana IL 61801', '201 N. Goodwin Avenue Urbana IL 61801']
};
var pyshell = new PythonShell('recommender.py', options);
pyshell.on('error', function (err) {
    console.log(err);
});
pyshell.on('message', function (message) {
    console.log(message);
});
**/

// Configs
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());

app.use('/', express.static('views/template'));

// router
var router = require('./router')(app);


module.exports = app;
app.listen(8000);
console.log("Safe Route Recommender");
console.log("Listening on port 8000");
