DEBUG = window.location.search.includes("debug=true")
const STATE = {
    NotPlaying: 0,
    InAnimation: 1,
    Playing: 2,
    MiddleAnimation: 3,
    OutAnimation: 4
}
window.cache = {}
window.handlers = {}
window.signals = {}
window.svgLoaded = false;
shouldBeStopped = false;
indexedDB.deleteDatabase('keyval-store');
get = (url) => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send();
    return JSON.parse(xhr.responseText);
}
const tl = gsap.timeline({ paused: true });
tl.from("body", { opacity: 0, duration: 1 })
tl.eventCallback("onComplete", () => { 
    tl.seek(0).pause(); shouldBeStopped = false; 
    window.parent.setRendererStopped();
})
showBody = () => document.querySelector("body").style.visibility = "visible";
play = () => tl.resume();
stop = () => { tl.resume(); shouldBeStopped = true; }
next = () => tl.resume();
checkForStop = () => { if(shouldBeStopped) { play(); } }
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
editSpanText = (textElementId, newTextArray) => {
    const textElement = document.getElementById(textElementId);
    if (!textElement) return;

    let currentX = 0;
    const tspans = textElement.querySelectorAll('tspan');
    let prevWidth;
    let prevX;

    tspans.forEach((tspan, index) => {
        if (index >= newTextArray.length) return;
        tspan.textContent = newTextArray[index];
        if (index > 0) {
            console.log(prevWidth)
            currentX += prevX + prevWidth + 10;
            tspan.setAttribute('x', currentX);
        }
        prevWidth = tspan.getComputedTextLength();
        prevX = parseFloat(tspan.getAttribute('x'));
    });
}

editSpanTextReverse = (textElementId, newTextArray) => {
    const textElement = document.getElementById(textElementId);
    if (!textElement) return;
    newTextReverse = newTextArray.reverse()
    const tspans = Array.from(textElement.querySelectorAll('tspan'));

    tspans.reverse().forEach((tspan, index) => {
        tspan.textContent = newTextReverse[index];
        console.log("index", index)
        if(index > 0) {
            let last = tspans[index - 1];
            let newX = last.getAttribute('x') - last.getComputedTextLength();
            tspan.setAttribute('x', newX);
        }
    });
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
// const LIVESTATS_URL = "http://localhost:8000/";
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

    window.setRunning = () => {
        sock.emit("setRendererRunning")
    }

    window.setStopped = () => {
        sock.emit("setRendererStopped")
    }
});