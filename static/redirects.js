
let track = (link, id) => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/click/"+ id );
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "link": link.dataset.track
        }));
}

let ratings = document.getElementsByName("star");

let rate = (link, id) => {
    let rating = 3;
    for (let i = 0; i < ratings.length; i++) {
        if (ratings[i].checked) {
            rating = ratings[i].value ;
        }
    }
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/rate/"+ id + "/" + rating );
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "rating": rating
        }));
}