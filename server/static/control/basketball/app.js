document.addEventListener('alpine:init', () => {
    Alpine.data("infoBarControl", () => {
        return {
            items: [{ title: "VENUE", subtitle: "DASKALAKIS ATHLETIC CENTER", color: "neutral" }],
            inputItem: { title: "", subtitle: "", color: "neutral" },
            selected: 0,
            fullText: (item) => item.title + " - " + item.subtitle + " - " + item.color,
            init() {
                this.items = get("infoBarItems") || this.items
            },
            update() {
                let item = this.items[this.selected];
                updateKey("Info-Bar-Title", item.title)
                updateKey("Info-Bar-Caption", item.subtitle)
                updateKey("sliderColor", item.color)
            },
            add() {
                this.items = [...this.items, this.inputItem]
                this.selected = this.items.length - 1
                cache("infoBarItems", this.items)
            },
            remove() {
                if(confirm("Are you sure you want to remove this item?")) {
                    this.items.splice(this.selected, 1)
                    this.selected = 0
                    cache("infoBarItems", this.items)
                }
            }
        }
    })

    Alpine.data("playerSliderControl", () => {
        return {
            side: "home",
            shirt: "0",
            update: () => {
                console.log(shirt, side)
            }
        }
    })
})

cache = (key, val) => localStorage.setItem(key, JSON.stringify(val))
get = (key) => JSON.parse(localStorage.getItem(key))

const LIVESTATS_URL = "https://livestats.gurleen.dev/";
const sock = io(LIVESTATS_URL);

sock.on("connect", () => {
    console.log("Connected to livestats.");
    sock.emit("get_store", (store) => {
        console.log(store)
    })

    sock.on("update", (payload) => {
        console.log(payload)
    })

    sock.on("signal", (payload) => {
        console.log("SIGNAL: ", payload)
    })

    window.emitSignal = (key) => {
        sock.emit("send_signal", { signal: key })
    }

    window.updateKey = (key, value) => {
        sock.emit("do_update", { "key": key, "value": value });
        payload = {}
        payload[key] = value
        console.log(payload)
    }
});