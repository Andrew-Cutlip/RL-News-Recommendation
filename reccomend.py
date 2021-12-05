# given state take action of recommendation with best values
import db.db as db
import numpy as np


# will want to initialize model based on saved weights on server start
def load_model():
    pass


def make_recommendation(last_clicks: list):
    pass


def random_articles(n: int):
    articles = db.get_all_articles()
    print(len(articles))
    print(type(articles))
    arts = np.array(articles)
    rand = arts[np.random.choice(len(articles), n, replace=False)]
    return rand


def add_source_names(articles: list):

    for article in articles:
        source_id = article[2]
        name = db.get_source_name(source_id)
        article[2] = name

    return articles


# save as json file maybe to store for training
def store_replays(last_clicks: list, reward: int, actions: list, results: list):
    pass
