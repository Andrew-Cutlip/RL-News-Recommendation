import db.db as db
import json


def insert_json(filename: str):
    with open(filename, 'r') as file:
        json_file = json.load(file)
        articles = json_file["articles"]


def add_sources(articles: list):
    sources = [article["source"]["name"] for article in articles]