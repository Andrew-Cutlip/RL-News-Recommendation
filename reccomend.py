# given state take action of recommendation with best values
import db.db as db
import numpy as np
import json


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
# calculate reward later
def store_replays(last_clicks: list,  actions: list, results: list):
    filename = "replays.json"
    with open(filename, "rw") as file:
        data = json.load(file)
        s1_list = data["s1"]
        s1_list.append(last_clicks)
        s2_list = data["s2"]
        s2_list.append(results)
        a_list = data["a"]
        a_list.append(actions)
        new_data = {"s1": s1_list, "a": a_list, "s2": s2_list}
        new_data_json = json.dumps(new_data)
        file.write(new_data_json)

