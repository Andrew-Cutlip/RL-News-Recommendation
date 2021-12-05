
def get_last_n_click(n: int, clicks: list) -> list:
    # need to supplement data
    if len(clicks) < n:
        pass
    else:
        last_clicks: list = clicks[0:n]
        return last_clicks
