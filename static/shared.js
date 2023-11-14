DEBUG = window.location.search.includes("debug=true")
window.cache = {}
window.handlers = {}
window.svgLoaded = false;
indexedDB.deleteDatabase('keyval-store');
const tl = gsap.timeline({ paused: true });
tl.eventCallback("onComplete", () => tl.seek(0).pause())
play = () => tl.resume();
stop = () => tl.pause().seek(0);
next = () => tl.resume();
setHandler = (key, callback) => handlers[key] = callback
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
doUpdate = (data) => {
    for (const [rawKey, value] of Object.entries(data)) {
        if (rawKey.includes(":")) {
            [prefix, key] = rawKey.split(":");
        }
        else {
            prefix = ""
            key = rawKey
        }
        window.cache[key] = value;
        if (key != "epochID") {
            handleKeyValue(prefix, key, value)
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
endAlignText = (k) => {
    elem = document.getElementById(k)
    width = elem.getBBox().width - 25
    gsap.to(`#${k}`, { duration: 0, x: `+=${width}` })
    elem.style.textAnchor = "end"
}
middleAlignText = (k) => {
    elem = document.getElementById(k)
    width = (elem.getBBox().width / 2)
    gsap.to(`#${k}`, { duration: 0, x: `+=${width}` })
    elem.style.textAnchor = "middle"
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

    window.updateKey = (key, value) => {
        sock.emit("do_update", { "key": key, "value": value });
        payload = {}
        payload[key] = value
        console.log(payload)
        window.doUpdate(payload)
    }
});