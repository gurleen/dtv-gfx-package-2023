indexedDB.deleteDatabase('keyval-store')
const tl = gsap.timeline({paused: true});
play = () => tl.play();
stop = () => tl.pause().seek(0);
updateText = (k, v) => document.querySelector(`#${k} > tspan`).innerHTML = v;
endAlignText = (k) => {
    elem = document.getElementById(k)
    width = elem.getBBox().width - 25
    gsap.to(`#${k}`, {duration: 0, x: `+=${width}`})
    elem.style.textAnchor = "end"
}