#! /usr/bin/env node

import WebSocket from 'ws';
import https from 'https';

const options = {
    hostname: 'https://localhost',
    port: 5000,
    method: 'GET',
    headers: {'User-Agent': 'Mozilla/5.0'},
    rejectUnauthorized: false
};

var message = 'smd+265598+{"fields":["31","83"]}'
var tic_message = 'tic'
console.log(message)
const ws = new WebSocket('wss://192.168.1.127:5000/v1/api/ws', {
    agent: new https.Agent(options)
});

const getDataWS = async function() {
    while (true) {
        setTimeout(ws.send, 1000, tic_message);
        console.log('sent')
}
}

ws.on('error', console.error)
ws.on('connect', function open() {
    getDataWS();
});

ws.on('message', function message(data) {
    console.log('received: %s', data)
});
