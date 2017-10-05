var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var path = require('path');
var fs = require('fs');
var querystring = require('querystring');
var url = require('url');
var mysql = require('mysql');
var express = require('express');
var appEx = express();
var connectionsArray = [];
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'door_interactive',
    port: 3306
  });
var POLLING_INTERVAL = 3000;
var pollingTimer;
var commonHeaders = {'Content-Type': 'text/html'};
var cssHeaders = {'Content-Type': 'text/css'};

//creating the server ( localhost:8000 )
app.listen(8000);

// If there is an error connecting to the database
// Maintain a hash of all connected sockets
var sockets = {}, nextSocketId = 0;

connection.connect(function(err) {
  // connected! (unless `err` is set)
  if (err) {
    console.log(err);
  }
});

// app.on('connection', function (socket) {
//   // Add a newly connected socket
//   var socketId = nextSocketId++;
//   sockets[socketId] = socket;
//   console.log('socket', socketId, 'opened');

//   // Remove the socket when it closes
//   socket.once('close', function () {
//     console.log('socket', socketId, 'closed');
//     delete sockets[socketId];
//   });

//   // Extend socket lifetime for demo purposes
//   socket.setTimeout(4000);
// });

// // Count down from 10 seconds
// (function countDown (counter) {
//   console.log(counter);
//   if (counter > 0)
//     return setTimeout(countDown, 1000, counter - 1);

//   // Close the server
//   app.close(function () { console.log('Server closed!'); });
//   // Destroy all open sockets
//   for (var socketId in sockets) {
//     console.log('socket', socketId, 'destroyed');
//     sockets[socketId].destroy();
//   }
// })(10);

// on server started we can load our client.html page
function handler(req, res) {   
    fs.readFile(__dirname + '/index.html', function(err, data) {
      if (err) {
        console.log(err);
        res.writeHead(500);
        return res.end('Error loading index.html');
      }
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(data);
    }); 
}


/*
 *
 * HERE IT IS THE COOL PART
 * This function loops on itself since there are sockets connected to the page
 * sending the result of the database query after a constant interval
 *
 */

var pollingLoop = function() {

  // Doing the database query
  var query = connection.query('SELECT * FROM door_log'),
    doorLogs = []; // this array will contain the result of our db query

  // setting the query listeners
  query
    .on('error', function(err) {
      // Handle error, and 'end' event will be emitted after this as well
      console.log(err);
      updateSockets(err);
    })
    .on('result', function(logs) {
      // it fills our array looping on each logs row inside the db
      doorLogs.push(logs);
    })
    .on('end', function() {
      // loop on itself only if there are sockets still connected
      if (connectionsArray.length) {

        pollingTimer = setTimeout(pollingLoop, POLLING_INTERVAL);

        updateSockets({
          doorLogs: doorLogs
        });
      } else {

        console.log('The server timer was stopped because there are no more socket connections on the app')

      }
    });
};


// creating a new websocket to keep the content updated without any AJAX request
io.sockets.on('connection', function(socket) {

  console.log('Number of connections:' + connectionsArray.length);
  // starting the loop only if at least there is one user connected
  if (!connectionsArray.length) {
    pollingLoop();
  }

  socket.on('disconnect', function() {
    var socketIndex = connectionsArray.indexOf(socket);
    console.log('socketID = %s got disconnected', socketIndex);
    if (~socketIndex) {
      connectionsArray.splice(socketIndex, 1);
    }
  });

  console.log('A new socket is connected!');
  connectionsArray.push(socket);

});

var updateSockets = function(data) {
  // adding the time of the last update
  data.time = new Date();
  console.log('Pushing new data to the clients connected ( connections amount = %s ) - %s', connectionsArray.length , data.time);
  // sending new data to all the sockets connected
  connectionsArray.forEach(function(tmpSocket) {
    tmpSocket.volatile.emit('notification', data);
  });
};

console.log('Please use your browser to navigate to http://localhost:8000');
