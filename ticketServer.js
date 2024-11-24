//@ts-check
"use strict";


const express = require("express");

const app = express();

const PORT = 80;

const fs = require("fs");
const http = require("http");
const https = require("https");

/*const SSL = {
    cert: fs.readFileSync("./.cert/fullchain.pem").toString("utf-8"),
    key: fs.readFileSync("./.cert/privkey.pem").toString("utf-8"),
};*/
const server = http.createServer(app);


app.get("/tickets/*", (req, res, next) => {
    const path = __dirname + req.path + ".html";
    
    if (fs.existsSync(path)){
        res.sendFile(path);
    } else {
        next();
    }
});


app.get(["/tmp/*", "/assets/*"], (req, res, next) => {
    const path = __dirname + req.path;
    if ((new URL(req.url, `http://${req.headers.host}`)).hostname != "cdn.kanokiw.com" || !fs.existsSync(path)){
        next();
        return;
    } else {
        res.sendFile(path);
    }
});


app.get("*", (req, res) => {
    res.status(404).sendFile(__dirname + "/index.html");
});


server.listen(8443, function(){
    console.log("ticket server is listening now: 8443")
});
