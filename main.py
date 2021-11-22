import json, secrets, string
import db.db as db

from flask import Flask, render_template, redirect, request, make_response, send_from_directory

app: Flask = Flask(__name__)

file = open("./data/general.json", "r")
general = json.load(file)


articles = general["articles"]

art_keys = enumerate(articles)

article_map = {
    i: article for i, article in enumerate(articles)
}


def make_cookie() -> str:
    alphabet = string.ascii_letters + string.digits
    cookie = ''.join(secrets.choice(alphabet) for i in range(32))
    return cookie


@app.route("/")
def home():
    print("Got Request")
    # make response
    response = make_response(render_template("News.html", articles=art_keys))
    cookies = request.cookies
    # check for user_id
    if "user_id" not in cookies:
        cookie = make_cookie()
        response.set_cookie("user_id", cookie)

    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # handle registration form data
        username = request.form["username"]
        print(username)
        password = request.form["password"]
        print(password)
        # want to check if username and password are good
        age = request.form["age"]
        print(age)
        gender = request.form["gender"]
        print(gender)
        general = request.form["g"]
        print(general)
        business = request.form["b"]
        print(business)
        entertainment = request.form["e"]
        print(entertainment)
        health = request.form["h"]
        print(health)
        science = request.form["sc"]
        print(science)
        sp = request.form["sp"]
        print(sp)

        return render_template("News.html")
    else:
        return render_template("Register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # process login
        username = request.form["username"]
        password = request.form["password"]

        # check this
    else:
        return render_template("Login.html")


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
    db.add_click(click)
    print("Got click")
    clicks = db.get_all_clicks()
    print(clicks)
    link = article["url"]

    # send to link
    return redirect(link)


@app.route("/static/<path:path>")
def send_static(path: str):
    return send_from_directory("./static", path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    print("Flask server Running!\n")

