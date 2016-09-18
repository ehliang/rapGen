var fs = require('fs')

module.exports = function(app, path) {
    app.get('/', function(req, res) {
        res.sendFile(__dirname + '/index.html');
    });

    var filepath = path.join(__dirname, 'thriftshop.mp3');

    app.get('/music', function(req, res){
    	console.log('here');
    	res.set({'Content-Type': 'audio/mpeg'});
    	var readStream = fs.createReadStream(filepath);
    	readStream.pipe(res);
    });
}
