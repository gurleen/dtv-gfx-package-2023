const LIVESTATS_URL = "https://livestats.gurleen.dev/";

const socket = io(LIVESTATS_URL);
socket.on("connect", () => {
    console.log("Connected to livestats.");
    socket.emit("get_store", (store) => {
        console.log(store)
    })
});
socket.on("disconnect", () => {
    console.error("Disconnected from livestats.");
})
socket.on("update", (payload) => {
        console.log(payload)
});

export let updateKey = (key, value) => {
    socket.emit("do_update", {"key": key, "value": value});
    console.log(`Updated ${key} to ${value}`)
}