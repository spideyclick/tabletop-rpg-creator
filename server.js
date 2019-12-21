var http = require('http');
var fs = require('fs');
var url = require('url');

http.createServer(function (req, res) {
	thisUrl = url.parse(req.url, true);
	if (thisUrl.pathname == '/scene.json') {
		fs.readFile('scene.json', function(err, data) {
			res.writeHead(200, { 'Content-Type': 'text/json' });
			res.write(data);
			res.end();
		});
	} else {
		fs.readFile('templates/engine.html', function (err, data) {
			res.writeHead(200, { 'Content-Type': 'text/html' });
			res.write(data);
			res.end();
		});
	};
	// res.writeHead(200, { 'Content-Type': 'text/html' });
	// res.end('Hello World!');
}).listen(8080);
