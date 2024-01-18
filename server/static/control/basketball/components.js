import van from "./van-1.2.7.min.js";

const {div, fieldset, legend} = van.tags;


export const Row = (...slot) => div({class: "row"}, ...slot)
export const Col = (...slot) => div({class: "col"}, ...slot)
export const Panel = (title, ...slot) => {
    return fieldset(
        legend(title),
        ...slot
    )
}