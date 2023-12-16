const LIVESTATS_URL = "http://localhost:8000/"
const sock = io(LIVESTATS_URL);


const STATE = {
    NotPlaying: 0,
    InAnimation: 1,
    Playing: 2,
    MiddleAnimation: 3,
    OutAnimation: 4
}

let currentGraphic = null;
let isGraphicPlaying = false;

getFrame = () => document.getElementById("layer0");

setRendererState = (state) => sock.emit("rendererState", state);
setRendererPlaying = () => sock.emit("setRendererRunning")
setRendererStopped = () => sock.emit("setRendererStopped")

sock.on("connect", () => {
    console.log("Connected to livestats.");
    sock.emit("rendererConnected");

    sock.on("rendererPlay", (graphicJson) => {
        let graphic = JSON.parse(graphicJson);
        console.log("Playing graphic: " + graphic.name + " (" + graphic.id + ")");
        frame = getFrame();
        console.log(graphic.template_file)
        frame.src = graphic.template_file;
        currentGraphic = graphic;
        frame.onload = () => {
            frame.contentWindow.setPlaying = setRendererPlaying;
            frame.contentWindow.setStopped = setRendererStopped;
            let data = {};
            graphic.global.forEach((x) => {
                data[x.key] = x.value;
            })
            graphic.vars.forEach((x) => {
                data[x.key] = x.value;
            });
            frame.contentWindow.update(JSON.stringify(data), delay=true);
            frame.contentWindow.play();
        }
    })

    sock.on("graphicVarsUpdated", (vars) => {
        console.log(vars);
        let data = {};
        vars.forEach((x) => {
            data[x.key] = x.value;
        });
        getFrame().contentWindow.update(JSON.stringify(data));
    })

    sock.on("rendererStop", () => {
        getFrame().contentWindow.stop();
    })

    sock.on("rendererNext", () => {
        getFrame().contentWindow.play();
    })

    sock.on("rendererBlank", () => {
        getFrame().onload = null;
        getFrame().src = "about:blank";
    })
});