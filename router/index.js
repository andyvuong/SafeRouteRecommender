module.exports = function (app) {
    app.use('/access', require('./routes/access'));
};