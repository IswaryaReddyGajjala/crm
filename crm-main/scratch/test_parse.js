// Mock window and navigator for the browserified SDK to load in Node
global.window = global;
Object.defineProperty(global, 'navigator', { value: { userAgent: "node" }, writable: true });

require('./scratch/vobiz-sdk.js');

// Since window.Vobiz is registered, let's see if we can find WebSocketInterface
// JsSIP might be inside window.Vobiz.client or we can inspect window/global keys
const keys = Object.keys(global);
const jsSIPKey = keys.find(k => k.toLowerCase().includes('jssip'));
console.log("Found keys:", keys.filter(k => k.includes('Vobiz') || k.toLowerCase().includes('sip')));

// Let's find how WebSocketInterface is exposed.
// Usually, it is exposed on the global or inside the Vobiz SDK class
try {
    const wsUrl = "wss://245d75820e7d11.lhr.life/vobiz-ws";
    // We can instantiate JsSIP WebSocketInterface directly if it is exposed.
    // Let's print window.Vobiz constructor or inspect it
    console.log("Vobiz constructor properties:", Object.getOwnPropertyNames(global.Vobiz));
} catch (e) {
    console.error("ERROR:", e);
}
