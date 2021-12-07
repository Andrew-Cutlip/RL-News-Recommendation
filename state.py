import db.db as db
import numpy as np


def get_last_n_click(n: int, clicks: list) -> list:
    # need to supplement data
    if len(clicks) < n:
        print("Getting random clicks")
        num_left = n - len(clicks)
        # get random clicks for the rest
        clicks = db.get_all_clicks()
        clicks = np.array(clicks)
        random = clicks[np.random.choice(len(clicks), num_left, replace=False)]
        print("Random clicks")
        print(random)
        if len(clicks) > 0:
            ret = clicks + random.tolist()
        else:
            ret = random.tolist()
        return ret

    else:
        last_clicks: list = clicks[-n:]
        return last_clicks
