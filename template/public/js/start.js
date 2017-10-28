/**
 * Created by PhpStorm.
 * User: rami
 * Date: 10/02/17
 * Time: 01:13
 */

var http = require('http');
var url  = require('url');
var fs   = require('fs'); 
var gpio = require('gpio');
var intervalTimer;

// Create and start web server on port 3000
var server = http.createServer(function (request, response) {

	var Connection = require('tedious').Connection;
	var config = {
		userName: 'root',
		password: '',
		server: 'localhost'
	};

	var connection = new Connection(config);
	connection.on('connect', function(err) {
		// If no error, then good to proceed.
		console.log("Connected");
	});

	// if (request.url == '/on') {
    //
	// 	onoff = 1;
	// 	response.end();
	//
	// } else if (request.url == '/off') {
    //
	// 	onoff = 0;
	// 	response.end();
	//
	// } else {
	// 	fs.readFile('./index.html', function(err, data) {
	// 		if (err) {
	// 			throw err;
	// 		}
	//
	// 		// Enable gpio 22
	// 		gpio22 = gpio.export(22, {
	// 		   ready: function() {
	// 			 // Set timer
	// 			 intervalTimer = setInterval(function() {
	//
	// 				if (onoff == 1) {
	// 					gpio22.set();
	// 				} else {
	// 					gpio22.reset();
	// 				}
	//
	// 			  }, 500);
	// 		   }
	// 		});
	//
	// 		// Write html output
	// 		response.writeHead(200, {"Content-Type": "text/html"});
	// 		response.end(data.toString() + '\n');
	// 	});
	// }

}); 

server.listen(3000);

// Cleanup on exit
// process.on('SIGINT', function() {
// 	console.log('\nexit, cleaning up...');
// 	clearInterval(intervalTimer);
//
// 	// Reset and release gpio port
// 	gpio22.reset();
//     	gpio22.unexport(function () {
// 		console.log('...done.');
// 		process.exit(0);
// 	});
// });
