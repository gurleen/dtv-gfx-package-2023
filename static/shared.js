indexedDB.deleteDatabase('keyval-store')
const tl = gsap.timeline({paused: true});
play = () => tl.play();
stop = () => tl.pause().seek(0);
updateText = (k, v) => document.querySelector(`#${k} > tspan`).innerHTML = v;
update = (data) => console.log(data)
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