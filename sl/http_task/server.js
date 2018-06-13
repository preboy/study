#!/usr/bin/node

let fs = require('fs');
let express = require('express');
let bodyParser = require("body-parser");

let app = express();

let commands = []
let ip_str=""


app.use(bodyParser.urlencoded({ extended: false }));


app.get('/task', function(req, res) {
    let str = commands.pop();
    if (str == undefined) {
        res.send("none");
    } else {
        // console.log("task:\t\t", str, commands.length);
        res.send(str);
        let d = new Date();
        let log = `DO COMMAND: '${str}' AT ${d}\n`
        fs.writeFileSync("web.log", log, {
            encoding: "utf8",
            flag: "a"
        });
    }
});


app.get('/push', function(req, res) {
    let str = req.query.command;
    commands.push(str)
        // console.log("push:\t\t", str, commands.length);
    res.send('OK');
});


app.get('/list', function(req, res) {
    res.json(commands);
});

// IP 地址自动更新
app.post('/ip', function(req, res) {
    let body = req.body;
    if (body.sign != "zhang") {
        res.end("fuck");
        return;
    }

    ip_str = req.connection.remoteAddress;
    res.end("ok");
});

app.get('/ip', function(req, res) {
    res.end(ip_str);
});

var server = app.listen(3000, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
});
