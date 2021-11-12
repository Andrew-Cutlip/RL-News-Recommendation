from flask import Flask, render_template

app: Flask = Flask(__name__)

articles = [
    {
        "title": "Test",
    },
    {
        "title": "Test2"
    }
]


@app.route("/")
def home():
    return render_template("News.html", articles=articles)


@app.route("/register")
def register():
    return "Registered"


@app.route("/login")
def login():
    return "Logged in"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

