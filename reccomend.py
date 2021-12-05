# given state take action of recommendation with best values
import db.db as db
import numpy as np
import json

config = {
    "num_episodes": 500,
    "batch_size": 256,
}


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
    with open(filename, "r") as file:
        data = json.load(file)
        if data is not  None:
            s1_list = data["s1"]
            s1_list.append(last_clicks)
            s2_list = data["s2"]
            s2_list.append(results)
            a_list = data["a"]
            a_list.append(actions)
        else:
            s1_list = [last_clicks]
            s2_list = [results]
            a_list = [actions]

        new_data = {"s1": s1_list, "a": a_list, "s2": s2_list}
        new_data_json = json.dumps(new_data)
    with open(filename, "w") as file:
        file.write(new_data_json)


def train_model():
    filename = "replays.json"
    with open(filename, "r") as file:
        replays = json.load(file)
    replay_buffer = [(s1, a, s2) for s1, a, s2 in zip(replays["s1"], replays["a"], replays["s2"])]
    buff = np.array(replay_buffer)
    episodes = config["num_episodes"]
    batch_size = config["batch_size"]
    for e in range(episodes):
        # sample replay buffer
        indices = np.random.choice(len(replay_buffer), batch_size, replace=False)
        batch = buff[indices]
