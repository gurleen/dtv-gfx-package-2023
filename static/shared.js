window.cache = {}
window.svgLoaded = false;
indexedDB.deleteDatabase('keyval-store');
const tl = gsap.timeline({paused: true });
tl.eventCallback("onComplete", () => tl.seek(0).pause())
play = () => tl.resume();
stop = () => tl.pause().seek(0);
next = () => tl.resume();
updateText = (k, v) => {
    element = document.querySelector(`#${k} > *`)
    if(element.tagName == "use") { k = element.getAttribute("xlink:href"); element = document.querySelector(`${k} > tspan`) }
    element.innerHTML = v;
}
updateColor = (k, v) => document.getElementById(k).setAttribute("fill", v)
updateImage = (k, v) => document.getElementById(k).setAttribute("xlink:href", v)
update = (data) => {
    if(!window.svgLoaded) {
        window.addEventListener("loaded", () => doUpdate(data), {once: true});
    } else { doUpdate(data); }
}
doUpdate = (data) => {
    for (const [key, value] of Object.entries(JSON.parse(data))) {
        console.log(key, value);
        window.cache[key] = value;
        if(key != "epochID") {
            try {
                if(key.startsWith("extra:")) {
                    window.handleExtra(key, value)
                }
                else {
                    updateText(key, value)
                }
            } catch(err) {
                console.error(err)
                console.error(key, value)
            }
        }
    }
}
endAlignText = (k) => {
    elem = document.getElementById(k)
    width = elem.getBBox().width - 25
    gsap.to(`#${k}`, {duration: 0, x: `+=${width}`})
    elem.style.textAnchor = "end"
}

createTemplateDefinition = (svg) => {
    def = {
        "description": "Top left with icon",
        "playserver": "OVERLAY",
        "playchannel": "1",
        "playlayer": "7",
        "webplayout": "7",
        "steps" : "1",
        "out": "manual",
        "uicolor": "2",
        "dataformat": "json",
    }
    def.description = svg.querySelector("title").innerHTML
    def.DataFields = []
    svg.querySelectorAll("text").forEach(x => {
        def.DataFields.push({field: x.id, ftype: "textfield", title: x.id, value: x.querySelector("tspan").innerHTML})
    })
    window.SPXGCTemplateDefinition = def
}