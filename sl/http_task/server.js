let express = require('express');
let app = express();

const fs = require('fs');

let commands = []

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


var server = app.listen(3000, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
});
