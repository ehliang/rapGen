var express = require('express');
var app = express();
var port = process.env.PORT || 9000;
var path = require('path');

// app.use(express.static(path.resolve("./src/")));

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
}); 

app.listen(port);
console.log("Sick beats in port  " + port);