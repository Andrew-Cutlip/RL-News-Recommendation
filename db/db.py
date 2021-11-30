import pymongo
import psycopg2

# client = pymongo.MongoClient("localhost", 27017)
conn = psycopg2.connect("dbname=rl user=postgres password=postgres")
cur = conn.cursor()
# db = client["test"]

# clicks = db.clicks

# noinspection SqlNoDataSourceInspection
tables = (
    """
    CREATE TABLE IF NOT EXISTS clicks (
        click_id INTEGER PRIMARY KEY NOT NULL,
        art_id INTEGER NOT NULL,
        source_id INTEGER NOT NULL,
        FOREIGN KEY (art_id) 
            REFERENCES articles (art_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sources ( 
        source_id INTEGER PRIMARY KEY NOT NULL,
        source_name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS articles ( 
        art_id INTEGER PRIMARY KEY NOT NULL,
        category_id INTEGER NOT NULL ,
        source_id INTEGER NOT NULL,
        author VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        content VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        FOREIGN KEY (category_id) 
            REFERENCES categories (category_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY,
        category_name VARCHAR(255) NOT NULL,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users ( 
        user_id INTEGER PRIMARY KEY,
        password_hash BYTE NOT NULL,
        age INTEGER NOT NULL,
        gender VARCHAR(255) NOT NULL,
        general_rate INT NOT NULL,
        business_rate INT NOT NULL,
        entertainment_rate INT NOT NULL,
        health_rate INT NOT NULL,
        science_rate INT NOT NULL,
        sports_rate INT NOT NULL
    )
    """
)

def add_click(click: dict):
    clicks.insert_one(click)


def get_all_clicks():
    all_clicks = clicks.find({})
    ret_val = [click for click in all_clicks]
    return ret_val
