#!/usr/bin/node

let express    = require('express');
var ex_session = require('express-session');
let app        = express();
let bodyParser = require("body-parser");
var path       = require('path');
let fs         = require('fs');
var morgan     = require('morgan');


let commands = []
let ip_str="none"


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use(morgan('common', {
    skip: function(req, res) { return res.statusCode < 400; },
}));


// static
app.use(express.static(path.join(__dirname, 'public')));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// session
app.use(ex_session({
    secret: 'fy admin key',
    resave: false,
    saveUninitialized: false,
    cookie: {
        maxAge: 3 * 3600 * 1000,
    }
}));


// ----------------------------------------------------------------

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


// view
app.get('/ipset', function(req, res) {
    res.render('ipset-view');
});


var server = app.listen(3000, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
});
