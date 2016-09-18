var fs = require('fs');
var python = require('python-shell');

module.exports = function(app, path) {
    app.get('/', function(req, res) {
        res.sendFile(__dirname + '/index.html');
    });

    var filepath = path.join(__dirname, 'python/thriftshop.mp3');

    app.get('/music', function(req, res) {
        res.set({ 'Content-Type': 'audio/mpeg' });
        var readStream = fs.createReadStream(filepath);
        readStream.pipe(res);
    });

    app.get('/genNew', function(req, res) {

        python.run('python/wrapper.py', function(err, success) {
            if (err) throw err;
            res.set({ 'Content-Type': 'audio/mpeg' });
            var readStream = fs.createReadStream(filepath);
            readStream.pipe(res);
        });

    });


}
