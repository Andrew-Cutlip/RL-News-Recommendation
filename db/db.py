import pymongo

client = pymongo.MongoClient()

db = client["test"]

clicks = db.clicks


def add_click(click: dict):
    clicks.insert_one(click)


def get_all_clicks():
    all_clicks = clicks.find({})
    return all_clicks
