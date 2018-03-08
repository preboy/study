/* 
sample: 
http://118.24.48.149:3000/push?command=shutdown /s /t 300
http://118.24.48.149:3000/push?command=shutdown /a
*/

let http = require("http")
let addr = "http://118.24.48.149:3000/push?command="
let args = 'shutdown /s /t 300'

http.get(addr + args, (res) => {
    // console.log(`task response: ${res.statusCode}`);
    // consume response body
    res.resume();

    let data = "";
    res.on('data', (d) => {
        data += d;
    }).on('end', () => {
        console.log("task:", data)
    })
}).on('error', (e) => {
    console.log(`Got error: ${e.message}`);
});