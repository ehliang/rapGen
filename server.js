var express = require('express');
var app = express();
var port = process.env.PORT || 9000;
var path = require('path');

app.use(express.static(path.resolve("./src/")));

require('./src/routes.js')(app, path);

app.listen(port);
console.log("Sick beats in port  " + port);