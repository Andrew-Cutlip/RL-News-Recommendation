
let track = (link, id) => {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/click/"+ id );
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "link": link.dataset.track
        }));
}


let rate = (e, id) => {
    let ratings = document.getElementsByName("star" + id);
    let rating = 3;
    for (let i = 0; i < ratings.length; i++) {
        if (ratings[i].checked) {
            rating = ratings[i].value ;
        }
    }
    console.log("Got rating on " + id + " of " + rating)
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/rate/"+ id + "/" + rating );
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
            "rating": rating
        }));
}

let formHandler = (e) => {
    e.preventDefault() ;
    return false;
}