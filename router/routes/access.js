/**
* Web app access routes for the python client-server
*/
var request = require('request');
var express = require('express');
var router = express.Router();

/**
* METHOD: POST
* PARAMS: {origin}, {destination}
* DESC: Takes two inputs from the user including their origin (location A) and their destination (location B).
* RETURNS: ...something...
*/
router.post('/map', function (req, res) {
    // catch error
    locationA = req.body.origin;
    locationB = req.body.destination;
    if(locationA === 'undefined' || locationB === 'undefined' || locationA.trim().length == 0 || locationB.trim().length == 0) {
        console.log("User input was invalid!");
        res.json({message: 'Error'});
    }
    else {
        /**
        * Other pre-processing here? Otherwise pass the parameters to our function
        */
        var payload = { origin: locationA, destination: locationB};
        request('/someroutehere',
                { json: true, body: payload },
                function(err, res, body) { // `body` is a js object if request was successful
                    console.log('Request Sent from Node Server');
        });
    }
});

module.exports = router;