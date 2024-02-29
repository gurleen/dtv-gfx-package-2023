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
                let text = `${item.title}  //  ${item.subtitle}`
                updateKey("fade:Generic-Slider-Text", text)
            },
            add() {
                this.items = [...this.items, deepCopy(this.inputItem)]
                this.selected = this.items.length - 1
                cache("infoBarItems", this.items)
            },
            remove() {
                if (confirm("Are you sure you want to remove this item?")) {
                    this.items.splice(this.selected, 1)
                    this.selected = 0
                    cache("infoBarItems", this.items)
                }
            }
        }
    })

    Alpine.data("playerSliderControl", (side) => {
        return {
            side: side == 1 ? "home" : "away",
            shirt: "0",
            player: null,
            teamInfo: null,
            statLine: null,
            playerImage: null,
            customText: "",
            update () {
                this.statLine = null
                this.player = null
                this.playerImage = null
                let teamInfo = ajax("/team-info")
                this.teamInfo = teamInfo
                let teamId = this.side == "home" ? teamInfo.home_id : teamInfo.away_id
                let player = ajax(`/teams/${teamInfo.sport}/${teamId}/players/${this.shirt}`)
                this.player = player
                this.playerImage = this.player ? `/headshot/${teamId}/${this.teamInfo.sport}/${this.shirt}` : ""
                this.statLine = ajax(`http://localhost:8081/player/${this.side}/${this.shirt}/line`).line ?? ""

                let side = this.side.charAt(0).toUpperCase() + this.side.slice(1)
                updateKey(`fade:${side}-Player-Name`, this.player.firstName + " " + this.player.lastName)
                updateKey(`fade:${side}-Player-Number`, this.player.jersey)
                updateKey(`fade:${side}-Player-Position`, this.player.position)
                updateKey(`img:${side}-Player-Headshot`, this.playerImage)
                updateKey(`fade:${side}-Player-Text`, this.customText == ""? this.statLine : this.customText)
            },
            toggle () {
                let side = this.side.charAt(0).toUpperCase() + this.side.slice(1)
                emitSignal(`${side}-Player-Slider:toggle`)
            }
        }
    })

    Alpine.data("comparisonControl", () => {
        return {
            selected: null,
            selectedProperName: null,
            items: STATS,
            homeStat: null,
            awayStat: null,
            properName: (item) => STATS_PROPER_NAME_MAP[item],
            update() {
                let box = ajax("http://localhost:8081/box")
                this.homeStat = box.home.team[this.selected]
                this.awayStat = box.away.team[this.selected]
                this.selectedProperName = STATS_PROPER_NAME_MAP[this.selected]

                updateKey("fade:Comparison-Slider-Stat", this.selectedProperName)
                updateKey("fade:Home-Comp-Stat", this.homeStat)
                updateKey("fade:Away-Comp-Stat", this.awayStat)
            }
        }
    })

    Alpine.data("teamSliderControl", (side) => {
        return {
            side: side == 1 ? "Home" : "Away",
            rawText: "",
            shouldFade: false,
            formattedText () {
                /*
                    Template string format: ... since/10:00
                */
                let split = this.rawText.split(" ")
                split.forEach((word, i) => {
                    if(word.startsWith("since/")) {
                        let sinceSplit = word.split("/")
                        let from = sinceSplit[1]
                        let to = window.CACHE["Clock"] ?? "00:00"
                        console.log(from, to)
                        split[i] = getTimeDifference(from, to)
                    }
                })
                return split.join(" ")
            },
            update() {
                let text = this.formattedText()
                let key = `${this.side}-Big-Text-Slider`
                if(this.shouldFade) { key = `fade:${key}` }
                updateKey(key, text)
            },
            toggle() {
                emitSignal(`${this.side}-Slider:toggle`)
            },
            init() {
                let funcName = `update${this.side}Slider`
                window[funcName] = () => {
                    if(this.rawText.includes("since/")) {
                        this.update()
                        document.querySelector(`#slider${this.side}FormattedText`).innerHTML = this.formattedText()
                    }
                }
            }
        }
    })
})

function deepCopy(obj) {
    return JSON.parse(JSON.stringify(obj))
}

function getTimeDifference(time1, time2) {
    /*
        time1 and time2 are strings in the format "10:00"
    */
    const [minutes1, seconds1] = time1.split(':').map(Number);
    const [minutes2, seconds2] = time2.split(':').map(Number);
    let totalSeconds1 = minutes1 * 60 + seconds1;
    let totalSeconds2 = minutes2 * 60 + seconds2;
    let diffInSeconds = Math.abs(totalSeconds1 - totalSeconds2);
    let minutes = Math.floor(diffInSeconds / 60);
    let seconds = diffInSeconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

const STATS = ['assists', 'blocks', 'blocks_received', 'efficiency', 'fast_break_points_made', 'field_goals', 'field_goals_attempted', 'field_goals_made', 'field_goals_percentage', 'fouls_on', 'fouls_personal', 'fouls_technical', 'free_throws', 'free_throws_attempted', 'free_throws_made', 'free_throws_percentage', 'minutes', 'plus_minus_points', 'points', 'points_fast_break', 'points_from_turnovers', 'points_in_the_paint', 'points_in_the_paint_made', 'points_second_chance', 'rebounds_defensive', 'rebounds_offensive', 'rebounds_total', 'second_chance_points_made', 'steals', 'three_pointers', 'three_pointers_attempted', 'three_pointers_made', 'three_pointers_percentage', 'turnovers', 'two_pointers_attempted', 'two_pointers_made', 'two_pointers_percentage']
const STATS_PROPER_NAME_MAP = {
    "assists": "Assists",
    "blocks": "Blocks",
    "blocks_received": "Blocks Received",
    "efficiency": "Efficiency",
    "fast_break_points_made": "Fast Break Points",
    "field_goals": "Field Goals",
    "field_goals_attempted": "Field Goals Attempted",
    "field_goals_made": "Field Goals Made",
    "field_goals_percentage": "Field Goals Percentage",
    "fouls_on": "Fouls On",
    "fouls_personal": "Fouls Personal",
    "fouls_technical": "Fouls Technical",
    "free_throws": "Free Throws",
    "free_throws_attempted": "Free Throws Attempted",
    "free_throws_made": "Free Throws Made",
    "free_throws_percentage": "Free Throws Percentage",
    "minutes": "Minutes",
    "plus_minus_points": "Plus Minus Points",
    "points": "Points",
    "points_fast_break": "Fast Break Points",
    "points_from_turnovers": "Points From Turnovers",
    "points_in_the_paint": "Points In The Paint",
    "points_in_the_paint_made": "Points In The Paint",
    "points_second_chance": "Second Chance Points",
    "rebounds_defensive": "Defensive Rebounds",
    "rebounds_offensive": "Offensive Rebounds",
    "rebounds_total": "Rebounds",
    "second_chance_points_made": "Second Chance Points",
    "steals": "Steals",
    "three_pointers": "Three Pointers",
    "three_pointers_attempted": "Three Pointers Attempted",
    "three_pointers_made": "Three Pointers Made",
    "three_pointers_percentage": "Three Pointers Percentage",
    "turnovers": "Turnovers",
    "two_pointers_attempted": "Two Pointers Attempted",
    "two_pointers_made": "Two Pointers Made",
    "two_pointers_percentage": "Two Pointers Percentage"
}

cache = (key, val) => localStorage.setItem(key, JSON.stringify(val))
get = (key) => JSON.parse(localStorage.getItem(key))

ajax = (url) => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send();
    return JSON.parse(xhr.responseText);
}

const LIVESTATS_URL = "https://livestats.gurleen.dev/";
const sock = io(LIVESTATS_URL);
window.CACHE = {}

sock.on("connect", () => {
    console.log("Connected to livestats.");
    sock.emit("get_store", (store) => {
        window.CACHE = store
        console.log(store)
    })

    sock.on("update", (payload) => {
        console.log(payload)
        window.CACHE[payload.key] = payload.value
        if(payload.key == "Clock") {
            window.updateHomeSlider()
            window.updateAwaySlider()
        }
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