const fs = require('fs');
const vm = require('vm');

const code = fs.readFileSync('./vobiz-sdk.cjs', 'utf-8');
const contextObject = {
    window: null,
    navigator: {
        userAgent: "Chrome", // Set as Chrome to pass browser checks
        platform: "linux",
        onLine: true, // Mock internet connection
        mediaDevices: {
            getUserMedia: () => Promise.resolve({}),
            enumerateDevices: () => Promise.resolve([])
        }
    },
    location: {
        toString: () => "https://localhost/",
        href: "https://localhost/",
        hostname: "localhost",
        protocol: "https:"
    },
    localStorage: {
        getItem: () => null,
        setItem: () => {},
        removeItem: () => {}
    },
    document: {
        createElement: () => ({
            setAttribute: () => {},
            style: {}
        }),
        getElementsByTagName: () => [],
        addEventListener: () => {},
        getElementById: () => null,
        querySelector: () => null,
        querySelectorAll: () => [],
        body: {
            appendChild: () => {}
        }
    },
    webkitSpeechRecognition: function() {},
    SpeechRecognition: function() {},
    RTCPeerConnection: function() {
        this.createOffer = () => Promise.resolve({});
        this.setLocalDescription = () => Promise.resolve({});
        this.close = () => {};
    },
    WebSocket: function(url, protocols) {
        console.log("\n[WebSocket Intercept] CONNECTING TO:", url, "WITH PROTOCOLS:", protocols, "\n");
        this.url = url;
        this.readyState = 0; // CONNECTING
        setTimeout(() => {
            this.readyState = 1; // OPEN
            if (this.onopen) this.onopen();
        }, 100);
        this.send = (data) => {
            console.log("[WebSocket Intercept] SEND DATA:", data);
        };
        this.close = () => {
            console.log("[WebSocket Intercept] CLOSED");
            this.readyState = 3; // CLOSED
            if (this.onclose) this.onclose({ wasClean: true });
        };
    },
    console: console
};
contextObject.window = contextObject;
contextObject.global = contextObject;

const context = vm.createContext(contextObject);
vm.runInContext(code, context);

const VobizClass = context.Vobiz;

if (VobizClass) {
    try {
        const client = new VobizClass({
            appId: "123",
            appSecret: "abc",
            registrationDomainSocket: "wss://245d75820e7d11.lhr.life/vobiz-ws"
        });
        
        console.log("Logging in...");
        client.client.on('onLogin', () => {
            console.log("SUCCESS: onLogin callback fired!");
        });
        
        client.client.on('onLoginFailed', (reason) => {
            console.log("FAILED: onLoginFailed callback fired:", reason);
        });
        
        client.client.login('play20106261801973454595480', 'Pwd24435299');
        
        // Keep process running for a short time to allow setTimeout callbacks to fire
        setTimeout(() => {
            console.log("Done testing login.");
        }, 1000);
        
    } catch (e) {
        console.error("ERROR during Vobiz initialization:", e);
    }
} else {
    console.log("Vobiz not found in context");
}
