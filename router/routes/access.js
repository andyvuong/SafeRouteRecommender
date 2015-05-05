var express = require('express');
var router = express.Router();

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
    locationA = req.body.origin;
    locationB = req.body.destination;
    if(locationA === 'undefined' || locationB === 'undefined' || locationA.trim().length == 0 || locationB.trim().length == 0) {
        console.log("User input was invalid!");
        res.json({message: 'Error'});
    }
    else {
        /**
        * Other pre-processing here? Otherwise pass the parameters to our function
        * ... more code later
        */
        
        // you're done if you see this!
        console.log("SUCCESS");
        res.json({message: 'Success'});
    }
});

module.exports = router;