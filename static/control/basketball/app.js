import van from "./van-1.2.7.min.js";
import { Panel, Row, Col } from "./components.js";
import { updateKey } from "./socket.js";

const { div, select, option, button, p, input } = van.tags;


const InfoBarControl = () => {
    const state = vanX.reactive({
        items: [{title: "Venue", subtitle: "Daskalakis Athletic Center"}, {title: "Date", subtitle: "2021-01-01"}],
        selected: 0,
        get selectedItem() { return this.items[this.selected] },
        showUpdated: false
    })

    const titleInput = input({type: "text"})
    const subtitleInput = input({type: "text"})

    return div(
        select(
            {onchange: e => { state.selected = e.target.value; }},
            ...state.items.map((item, idx) => option({value: idx}, `${item.title} - ${item.subtitle}`)),
        ),
        button({onclick: () => { 
            updateKey("sliderColor", "neutral")
            updateKey("Info-Bar-Title", state.selectedItem.title)
            updateKey("Info-Bar-Caption", state.selectedItem.subtitle)
            state.showUpdated = true;
            setTimeout(() => { state.showUpdated = false; }, 1000);
        }}, "Update"),
        state.showUpdated ? p("Updated") : null,
        Row(
            titleInput,
            subtitleInput,
            button({onclick: () => {
                state.items = [...state.items, ({title: titleInput.value, subtitle: subtitleInput.value})]
                console.log(state.items)
            }}, "Add")
        )
    )
}


const BasketballControl = () => {
    return Panel("Info Bar", 
        InfoBarControl()
    )
}

van.add(document.body, BasketballControl());