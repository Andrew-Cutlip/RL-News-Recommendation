# given state take action of recommendation with best values
import db.db as db
import numpy as np
import json
import reward
import tensorflow as tf
from keras import backend as k
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Input
import typing

total_num_articles = 3757
config = {
    "num_episodes": 500,
    "batch_size": 256,
    "input_size": 80,
    "output_size": total_num_articles,
    "alpha": 0.01,
    "recommendation_size": 10,
    "gamma": 0.99
}


def deep_q_network(input_shape, output_shape, lr) -> Sequential:
    deep = Sequential()

    deep.add(Dense(64, activation="relu", input_dim=input_shape))
    deep.add(Dense(32, activation="relu"))
    deep.add(Dense(output_shape, activation="linear"))

    deep.compile(loss="mse", optimizer=Adam(learning_rate=lr))

    return deep


def create_actor(input_shape, output_shape, lr) -> Sequential:
    actor = Sequential()
    actor.add(Input(input_shape, ))
    actor.add(Dense(128, activation="relu"))
    actor.add(Dense(64, activation="relu"))
    actor.add(Dense(output_shape, activation="Softmax", dtype="float64"))
    actor.compile(optimizer=Adam(lr), loss=actor_loss)

    return actor


def actor_loss(advantages, actions):
    clipped_act = k.clip(actions, 1e-8, 1 - 1e-8)
    # print(advantages.shape)
    # print(clipped_act.shape)
    losses = (- clipped_act * advantages)
    loss = tf.math.reduce_mean(losses)
    return loss


def create_critic(input_shape, output_shape, lr) -> Sequential:
    critic = Sequential()
    critic.add(tf.keras.Input(shape=(input_shape ,)))
    critic.add(Dense(128, activation='relu'))  # Hidden layer.
    critic.add(Dense(64, activation='relu'))  # Hidden layer.
    critic.add(Dense(output_shape , activation='linear'))  # Output layer.
    critic.compile(optimizer=Adam(learning_rate=lr), loss="mse")
    return critic


# model = deep_q_network(config["input_size"], config["output_size"], config["alpha"])

actor = create_actor(config["input_size"], config["output_size"], config["alpha"])
critic = create_critic(config["input_size"], 1, config["alpha"])
optimizer = Adam(config["alpha"])

# will want to initialize model based on saved weights on server start
def load_model():
    pass


def get_article_info(article_id: int):
    article = db.get_article_by_id(article_id)
    cat_id = article[1]
    source_id = article[2]

    return cat_id, source_id


def get_inputs(clicks: list) -> list:
    inputs = []
    for click in clicks:
        click_id = click[0]
        art_id = click[1]
        cat_id , source_id = get_article_info(art_id)
        # need to get information from articles
        client_id = click[2]
        clicked = click[3]
        rated = click[4]
        list_number = click[5]
        if rated:
            rating = click[6]
        else:
            rating = 0

        input_c = [click_id, art_id, cat_id, client_id, clicked, rated, list_number, rating]
        inputs.append(input_c)

    print(inputs)

    return inputs


def get_best_n_articles(values: list, n: int):
    # get indices of n largest values
    indices = np.argpartition(values, - n)[- n:]

    # these will be the article ids
    return indices


def make_recommendation(last_clicks: list):
    # will want to load model here if available
    print(last_clicks, flush=True)
    inputs: list = get_inputs(last_clicks)
    print(inputs, flush=True)
    # need to flatten inputs
    inputs: np.ndarray = np.array(inputs)
    print(inputs.shape, flush=True)
    inputs: np.ndarray = inputs.flatten()
    print(inputs, flush=True)
    print(inputs.shape, flush=True)
    inputs = inputs.reshape((-1, inputs.shape[0]))
    print(inputs, flush=True)
    inputs = tf.constant(inputs)
    # get values from model
    # action_vals = model.predict(inputs)
    action_vals = actor.predict(inputs)
    # will probably need to extract article ids somehow
    best_article_ids = get_best_n_articles(action_vals, config["recommendation_size"])
    print(best_article_ids, flush=True)
    # need to get articles from db and return them
    best_articles = db.articles_by_ids(best_article_ids)

    return best_articles, best_article_ids, action_vals


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
        if data is not None:
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
    all_rewards = []
    for e in range(episodes):
        # sample replay buffer
        indices = np.random.choice(len(replay_buffer), batch_size, replace=False)
        batch = buff[indices]
        with tf.GradientTape() as tape:
            values = tf.zeros(batch_size)
            all_probs = tf.zeros(batch_size)
            advantages = tf.zeros(batch_size)
            rewards = tf.zeros(batch_size)
            for i, sample in enumerate(batch):
                client_id = sample[0][2]
                recommend = sample[2]
                state = sample[0]
                value = critic.predict(state)
                values[i] = value
                next_value = critic.predict(recommend)
                # need to get actual clicks from click_ids
                reward_val = reward.calculate_reward(client_id, recommend)
                print(reward_val)
                rewards[i] = reward_val
                target = reward_val + config["gamma"] * next_value
                advantage = target - value
                advantages[i] = advantage

                probs = sample[1]

                log_probs = tf.math.log(probs)
                all_probs[i] = log_probs

            critic.fit(values, advantages)

            loss = actor_loss(advantages, all_probs)
            print(loss)

            # need to update actor weights too
            a_vars = actor.trainable_variables
            a_grad = tape.gradient(loss, a_vars)
            optimizer.apply_gradients(zip(a_grad, a_vars))

            all_rewards.append(rewards)

    return all_rewards
