const express = require('express');
const app = express();
const restRouter = require('./routes/rest');
const mongoose = require('mongoose');
const path = require('path');


//Connect to Mongo Database
mongoose.connect('mongodb://qichen90:cs5036@ds125068.mlab.com:25068/problems-db',{ useNewUrlParser: true } );
var db = mongoose.connection;
db.on('error', function() { 
    console.log("Unable to Connect");
});
db.once('open', function() {
    console.log("Connected Successfully");
});


// Support Cross Region
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});


//Register API 
app.use('/api/v1', restRouter);


//Provide main html
app.use(express.static(path.join(__dirname,'/public')));

app.use(function(req, res){

//   res.send('index.html',{root: path.join(__dirname, '/public') });
    res.send('index.html');
 
});



app.listen(3000, function() {
    console.log('Example app listening on port 3000!');
});
