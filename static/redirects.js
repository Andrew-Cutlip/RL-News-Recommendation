
let track = (link, id) => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/click/"+ id );
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "link": link.dataset.track
        }));
}