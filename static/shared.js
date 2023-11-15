DEBUG = window.location.search.includes("debug=true")
window.cache = {}
window.handlers = {}
window.signals = {}
window.svgLoaded = false;
indexedDB.deleteDatabase('keyval-store');
const tl = gsap.timeline({ paused: true });
tl.from("body", { opacity: 0, duration: 0.5 })
tl.eventCallback("onComplete", () => tl.seek(0).pause())
play = () => tl.resume();
stop = () => tl.resume();
next = () => tl.resume();
setHandler = (key, callback) => handlers[key] = callback
signal = (key, callback) => signals[key] = callback
getTextElement = (k) => {
    element = document.querySelector(`#${k} > *`)
    if (element != null) {
        if (element.tagName == "use") { k = element.getAttribute("xlink:href"); element = document.querySelector(`${k} > tspan`) }
        return element
    }
}
updateText = (k, v) => { getTextElement(k).innerHTML = v; }
fadeText = (k, v) => {
    element = getTextElement(k)
    if (element.innerHTML == v) { return; }
    ftl = gsap.timeline({ paused: true })
    ftl.to(element, { duration: 0.2, opacity: 0 })
        .call(updateText, [k, v], ">")
        .to(element, { duration: 0.2, opacity: 1 })
        .play()
}
fadeGivenElementText = (element, v) => {
    if (element.innerHTML == v) { return; }
    ftl = gsap.timeline({ paused: true })
    ftl.to(element, { duration: 0.2, opacity: 0 })
        .call(updateText, [k, v], ">")
        .to(element, { duration: 0.2, opacity: 1 })
        .play()
}
fadeOn = (k) => { gsap.to(`#${k}`, { opacity: 1, duration: 0.5 }) }
fadeOff = (k) => { gsap.to(`#${k}`, { opacity: 0, duration: 0.5 }) }
setVisibility = (k, v) => {
    k = k.replace("show:", "")
    v ? fadeOn(k) : fadeOff(k)
}
updateColor = (k, v) => document.getElementById(k).setAttribute("fill", v)
updateImage = (k, v) => document.getElementById(k).setAttribute("xlink:href", v)
update = (data) => {
    parsed = JSON.parse(data);
    if (!window.svgLoaded) {
        window.addEventListener("loaded", () => { doUpdate(parsed) }, { once: true });
    } else { doUpdate(parsed); }
}
parseKey = (rawKey) => {
    if (rawKey.includes(":")) {
        [prefix, key] = rawKey.split(":");
    }
    else {
        prefix = ""
        key = rawKey
    }
    return {prefix: prefix, key: key}
}
doUpdate = (data) => {
    for (const [rawKey, value] of Object.entries(data)) {
        parsed = parseKey(rawKey)
        window.cache[key] = value;
        if (key != "epochID") {
            handleKeyValue(parsed.prefix, parsed.key, value)
        }
    }
}
handleKeyValue = (prefix, key, value) => {
    try {
        if (key in handlers) {
            handlers[key](value);
        }
        else if (prefix == "extra") {
            window.handleExtra(key, value)
        }
        else if (prefix == "img") {
            window.updateImage(key, value)
        }
        else if (prefix == "color") {
            window.updateColor(key, value)
        }
        else if (prefix == "fade") {
            fadeText(key, value)
        }
        else if (prefix == "show") {
            setVisibility(key, Boolean(Number(value)))
        }
        else if(prefix == "live") {
            updateKey(key, value)
        }
        else {
            updateText(key, value)
        }
    } catch (err) {
        if (DEBUG) {
            console.error(err)
            console.error(key, value)
        }
    }
}
endAlignText = (k, x) => {
    elem = document.getElementById(k)
    elem.style.textAnchor = "end"
    tspan = getTextElement(k)
    tspan.setAttribute("x", x)
}
middleAlignText = (k, x) => {
    elem = document.getElementById(k)
    elem.style.textAnchor = "middle"
    tspan = getTextElement(k)
    tspan.setAttribute("x", x)
}

createTemplateDefinition = (svg) => {
    def = {
        "description": "Top left with icon",
        "playserver": "OVERLAY",
        "playchannel": "1",
        "playlayer": "7",
        "webplayout": "7",
        "steps": "1",
        "out": "manual",
        "uicolor": "2",
        "dataformat": "json",
    }
    def.description = svg.querySelector("title").innerHTML
    def.DataFields = []
    svg.querySelectorAll("text").forEach(x => {
        def.DataFields.push({ field: x.id, ftype: "textfield", title: x.id, value: x.querySelector("tspan").innerHTML })
    })
    window.SPXGCTemplateDefinition = def
}

const LIVESTATS_URL = "https://livestats.gurleen.dev/";
const sock = io(LIVESTATS_URL);

sock.on("connect", () => {
    console.log("Connected to livestats.");
    sock.emit("get_store", (store) => {
        console.log(store)
        window.doUpdate(store)
    })

    sock.on("update", (payload) => {
        parsed = parseKey(payload.key)
        console.log(parsed.prefix, parsed.key, payload.value)
        handleKeyValue(parsed.prefix, parsed.key, payload.value)
    })

    sock.on("signal", (payload) => {
        console.log("SIGNAL: ", payload)
        func = signals[payload.key]
        func()
    })

    window.emitSignal = (key) => {
        sock.emit("send_signal", {signal: key})
    }

    window.updateKey = (key, value) => {
        sock.emit("do_update", { "key": key, "value": value });
        payload = {}
        payload[key] = value
        console.log(payload)
        window.doUpdate(payload)
    }
});