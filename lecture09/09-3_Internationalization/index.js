var express = require("express");
var app = express();
var hostname = "127.0.0.1";
var port = 8090;

app.use(express.static('.'));

app.listen(port, hostname);