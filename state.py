import db.db as db
import numpy as np


def get_last_n_click(n: int, clicks: list) -> list:
    # need to supplement data
    if len(clicks) < n:
        print("Getting random clicks")
        # get random clicks for the rest
        clicks = db.get_all_clicks()
        clicks = np.array(clicks)
        random = clicks[np.random.choice(len(clicks), n, replace=False)]
        print("Random clicks", flush=True)
        print(random, flush=True)
        print("Clicks", flush=True)
        print(clicks, flush=True)
        ret = random.tolist()
        return ret

    else:
        last_clicks: list = clicks[-n:]
        return last_clicks
