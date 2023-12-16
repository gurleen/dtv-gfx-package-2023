const LIVESTATS_URL = "https://livestats.gurleen.dev/";
//const LIVESTATS_URL = "http://localhost:8000/";

const VALUE_MAPPERS = {
    "img": "updateImage",
    "color": "updateColor",
    "fade": "fadeText",
    "show": "setVisibility",
    "playAnim": "playAnimation"
}

function getMapperFunc(prefix) {
    let mapperName = VALUE_MAPPERS[prefix];
    let mapper = window[mapperName] || window["updateText"];
    return mapper;
}

function parsePayload(rawKey, value) {
    [prefix, key] = rawKey.split(":");
    mapper = getMapperFunc(prefix);
    if(key in (window.handlers || {})) { mapper = window.handlers[key](value); }
    try {
        console.log(prefix, key, value);
        mapper(key, value);
    } catch (error) {
        console.error(error);
    }   
}

function handlePayload(payload) {
    console.log(payload)
    if(payload.key.includes(":")) { parsePayload(payload.key, payload.value) }
    else { window.updateText(payload.key, payload.value) }
}

function fullUpdate(store) {
    for([key, value] of Object.entries(store)) {
        handlePayload({"key": key, "value": value})
    }
}

function PluginInstance() {
    this.init = () => {
        this.store = {};
        const sock = io(LIVESTATS_URL);
        this.sock = sock;
        sock.on("connect", () => {
            console.log("Connected to livestats.");
            sock.emit("get_store", (store) => {
                this.store = store
                console.log(store)
                setTimeout(() => fullUpdate(store), 500)
            })
            window.updateFromStore = function () {
                fullUpdate(this.store)
            }
            window.getStore = function () {
                return this.store;
            }
        });
        sock.on("disconnect", () => {
            console.error("Disconnected from livestats.");
        })
        sock.on("update", (payload) => {
                // this.updateValue(payload.key, payload.value);
                handlePayload(payload)
                [prefix, key] = payload.key.split(":");
                print(key)
                this.store[key] = payload.value;
                console.log(payload)
        });
    }

    this.updateValue = (key, value) => {
        handlePayload({key: key, value: value})
    }

    window.updateKey = (key, value) => {
        this.sock.emit("do_update", {"key": key, "value": value});
        this.updateValue(key, value)
    }
}

var plugin = plugin || new PluginInstance;
plugin.init();
