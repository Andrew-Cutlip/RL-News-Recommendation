import json, secrets, string

import db.db as db
import state
import recommend
import sys
import data.insert as insert
from flask import Flask, render_template, redirect, request, make_response, send_from_directory

app: Flask = Flask(__name__)


def make_cookie() -> str:
    alphabet = string.ascii_letters + string.digits
    cookie = ''.join(secrets.choice(alphabet) for i in range(32))
    return cookie


@app.route("/")
def home():
    print("Got Request")
    cookies = request.cookies
    if "user_id" in cookies:
        cookie = cookies["user_id"]
        client = db.get_client_by_cookie(cookie)
        print(client)
        client_id = client[0]
        is_user = client[2]
        num_clicks = 10
        clicks = db.get_user_clicks(client_id)
        last_clicks = state.get_last_n_click(num_clicks, clicks)
        if is_user:
            # got logged in user
            print("Logged in user")
            # probably want to get all clicks maybe from multiple clients for one user
    else:
        cookie = make_cookie()
        # need to add to client db
        is_user = False
        client = {
            "is_user": is_user,
            "cookie": cookie
        }
        db.insert_client(client)
        # need to get clicks for starting state
        last_clicks = []
    arts = 10
    # will want articles chosen by model
    # rand = recommend.random_articles(arts)
    # articles = recommend.add_source_names(rand)
    # print("Random articles\n")
    # print(rand)
    print("Last clicks")
    print(last_clicks, flush=True)
    rec = recommend.make_recommendation(last_clicks)
    articles = recommend.add_source_names(rec)

    client = db.get_client_by_cookie(cookie)
    client_id = client[0]
    # need to add clicks for articles in db
    clicks = []
    actions = []
    for i, article in enumerate(articles):
        click = {}
        click["art_id"] = article[0]
        click["client_id"] = client_id
        click["position"] = i

        click_id = db.insert_click(click)
        clicks.append(click_id)
        actions.append(article[0])

    # add to experience replay
    recommend.store_replays(last_clicks, actions, clicks)
    # make response
    response = make_response(render_template("News.html", articles=articles))
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
        # hash password
        # need to update client in db and add to users
        user = {
            "password": password,
            "age": age,
            "gender": gender,
            "e": entertainment,
            "b": business,
            "g": general,
            "h": health,
            "sc": science,
            "sp": sp
        }
        user_id = db.insert_user(user)
        db.register_client(user_id)

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


@app.route("/click/<int:key>", methods=["POST"])
def click(key: int):
    print("Got click", flush=True)
    # just need to update click already in db
    article = db.get_article_by_id(key)
    print("article")
    # print(article, flush=True)
    # need to save user click
    user_id = request.cookies.get("user_id")
    # check if logged in
    client = db.get_client_by_cookie(user_id)
    client_id = client[0]
    db.set_click(key, client_id)
    print("Got click")
    res = make_response(("", 204))
    return res


@app.route("/rate/<int:key>/<int:rating>", methods=["POST"])
def rate(key: int, rating: int):
    article = db.get_article_by_id(key)
    user_id = request.cookies.get("user_id")
    client = db.get_client_by_cookie(user_id)
    client_id = client[0]
    # get rating somehow
    db.set_rating(rating, key, client_id)
    print("Rated")
    res = make_response(("", 204))
    return res


@app.route("/static/<path:path>")
def send_static(path: str):
    return send_from_directory("./static", path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    # db.drop_articles()
    # need to drop click for new format
    # db.drop_clicks()
    db.create_tables(db.tables)
    # add stuff to db.
    prefix = "data/"
    files = [
        prefix + "businessc.json" ,
        prefix + "entertainmentc.json" ,
        prefix + "generalc.json" ,
        prefix + "healthc.json" ,
        prefix + "sciencec.json" ,
        prefix + "sportsc.json" ,
        prefix + "technologyc.json"
    ]
    categories = [
        "business" ,
        "entertainment" ,
        "general" ,
        "health" ,
        "science" ,
        "sports" ,
        "technology"
    ]
    # articles = insert.open_articles(files , categories)
    # insert.add_articles(articles)
    app.run(host="0.0.0.0", port=port)
    print("Flask server Running!\n")

