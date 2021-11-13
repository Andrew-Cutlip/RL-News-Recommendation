import json, secrets, string

from flask import Flask, render_template, redirect, request, make_response

app: Flask = Flask(__name__)

file = open("./data/general.json", "r")
general = json.load(file)


articles = general["articles"]

art_keys = enumerate(articles)

article_map = {
    i: article for i, article in enumerate(articles)
}

clicks = []


def make_cookie() -> str:
    alphabet = string.ascii_letters + string.digits
    cookie = ''.join(secrets.choice(alphabet) for i in range(32))
    return cookie


@app.route("/")
def home():
    # make response
    response = make_response(render_template("News.html", articles=art_keys))
    cookies = request.cookies
    # check for user_id
    if "user_id"  not in cookies:
        cookie = make_cookie()
        response.set_cookie("user_id", cookie)

    return response


@app.route("/register")
def register():
    return "Registered"


@app.route("/login")
def login():
    return "Logged in"


@app.route("/click/<int:key>")
def click(key: int):
    article = article_map[key]
    source = article["source"]
    # need to save user click
    id = request.cookies.get("user_id")
    click = {
        "user_id": id,
        "art_key": key,
        "source": source["name"]
    }
    clicks.append(click)
    print("Got click")
    print(clicks)
    link = article["url"]

    # send to link
    return redirect(link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

