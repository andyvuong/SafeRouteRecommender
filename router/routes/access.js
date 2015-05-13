var express = require('express');
var router = express.Router();
var PythonShell = require("python-shell");

var PythonShell = require('python-shell');


router.post('/test', function (req, res) { 
    console.log(req.body.fname);
    res.send({message: 'successful'});
});


/**
* METHOD: POST
* PARAMS: {origin}, {destination}
* DESC: Takes two inputs from the user including their origin (location A) and their destination (location B).
* RETURNS: ...something...
*/
router.post('/map', function (req, res) {
    // catch error
    locationA = req.body.src;
    locationB = req.body.dest;
    if(locationA === 'undefined' || locationB === 'undefined' || locationA.trim().length == 0 || locationB.trim().length == 0) {
        console.log("Error: User input was invalid!");
        res.json({message: 'Error'});
    }
    else {
        /**
        * Other pre-processing here? Otherwise pass the parameters to our function
        * ... more code later
        */
        var options = {
            mode: 'text',
            scriptPath: '.',
            args: [locationA, locationB]
        };
        var pyshell = new PythonShell('recommender_01.py', options);
        // message handlers
        pyshell.on('error', function (err) {
            console.log("Error: Python Shell Error");
            console.log(err);
            res.json({message: 'Error'});
        });
        pyshell.on('message', function (data) {
            console.log(data);
            if(data === 'Error') {
                console.log("Script ran successfully but there was an error!");
                res.json({message: 'Error'});
            }
            else {
                // serve map
                console.log("SUCCESS");
                var data_remove = data.replace("[", "").replace("]", "");
                var data_split = data_remove.split("),");
                for(i=0; i<data_split.length; i++) {
                    data_split[i] = data_split[i].replace(" ", "");
                    if(data_split[i].indexOf(')') < 0 ) {
                        data_split[i] = data_split[i] + ')';
                    }
                }
                res.json({message: 'Success', route: data_split});
            }
        });
    }
});

module.exports = router;