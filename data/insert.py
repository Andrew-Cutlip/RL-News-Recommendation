import db.db as db
import json


def insert_json(filename: str):
    with open(filename, 'r') as file:
        json_file = json.load(file)
        articles = json_file["articles"]


def open_articles(filenames: list, categories: list) -> list:
    articles = []
    for filemame, category in zip(filenames, categories):
        with open(filemame, 'r') as file:
            json_f = json.load(file)
            arts = json_f["articles"]
            for art in arts:
                art["category"] = category
            articles += arts

    return articles


def add_sources(articles: list):
    sources = [article["source"]["name"] for article in articles]

    distinct = set(sources)

    db.insert_sources(list(distinct))


def add_categories(categories: list):
    for category in categories:
        db.insert_category(category)


def add_articles(articles: list):
    db.insert_articles(articles)


if __name__ == "__main__":
    prefix = "./"
    files = [
        prefix + "businessc.json",
        prefix + "entertainmentc.json",
        prefix + "generalc.json",
        prefix + "healthc.json",
        prefix + "sciencec.json",
        prefix + "sportsc.json",
        prefix + "technologyc.json"
    ]
    categories = [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology"
    ]
    articles = open_articles(files, categories)

    add_sources(articles)

