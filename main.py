import json

from flask import Flask, render_template, redirect

app: Flask = Flask(__name__)

file = open("./data/general.json", "r")
general = json.load(file)


articles = general["articles"]

art_keys = enumerate(articles)

article_map = {
    i: article for i, article in enumerate(articles)
}


@app.route("/")
def home():
    return render_template("News.html", articles=art_keys)


@app.route("/register")
def register():
    return "Registered"


@app.route("/login")
def login():
    return "Logged in"


@app.route("/click/<int:key>")
def click(key: int):
    article = article_map[key]
    # need to save user click
    print("Got click")
    link = article["url"]

    # send to link
    return redirect(link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

