var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');
var path = require("path");
var pythonShell = require("python-shell");

var app = express();

// Configs
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());

app.use('/', express.static('views/template'));
//app.get('/',function(req,res){
//    res.sendFile(path.join(__dirname+'/views/template/index.html'));
//});

// router
var router = require('./router')(app);


module.exports = app;
app.listen(8000);
console.log("Safe Route Recommender");
console.log("Listening on port 8000");
