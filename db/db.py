import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client["test"]

clicks = db.clicks


def add_click(click: dict):
    clicks.insert_one(click)


def get_all_clicks():
    all_clicks = clicks.find({})
    ret_val = [click for click in all_clicks]
    return ret_val
