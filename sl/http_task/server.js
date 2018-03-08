var express = require('express');
var app = express();


let commands = []


app.get('/task', function (req, res) {
    let str = commands.pop();
    if (str == undefined){
        res.send("none");
    }
    // console.log("task:\t\t", str, commands.length);
    res.send(str);
});


app.get('/push', function (req, res) {
    let str = req.query.command;
    commands.push(str)
    // console.log("push:\t\t", str, commands.length);
    res.send('OK');
});



var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
});
