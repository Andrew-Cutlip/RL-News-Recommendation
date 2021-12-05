# given state take action of recommendation with best values
import db.db as db
import numpy as np


def make_recommendation(last_clicks: list):
    pass


def random_articles(n: int):
    articles = db.get_all_articles()
    print(articles)
    rand = np.random.choice(articles, n, replace=False)
    return rand

