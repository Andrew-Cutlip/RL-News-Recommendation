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
        click_id SERIAL PRIMARY KEY NOT NULL,
        art_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        clicked BOOLEAN NOT NULL,
        FOREIGN KEY (art_id) 
            REFERENCES articles (art_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sources ( 
        source_id SERIAL PRIMARY KEY NOT NULL,
        source_name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS articles ( 
        art_id SERIAL PRIMARY KEY NOT NULL,
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
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(255) NOT NULL,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users ( 
        user_id SERIAL PRIMARY KEY,
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
    """,
    """
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            cookie VARCHAR(255) NOT NULL,
            is_user BOOLEAN NOT NULL,
            user_id INTEGER  
        )
    """
)


def insert_click(click: dict):
    # need to insert a click with client id , article id
    sql = """ INSERT INTO clicks
    VALUES (%s, %s)
    """
    cur.execute(sql, (click["client_id"], click["art_id"]))

    conn.commit()


def get_user_clicks(client_id: int):
    sql = """
        SELECT * FROM clicks
        WHERE client_id = (%s)
    """

    cur.execute(sql, client_id)

    conn.commit()


def insert_articles(articles: list):
    sql = """
        INSERT INTO articles
        
    """


def insert_client(client: dict):
    sql = """
        INSERT INTO clients
        VALUES (%s, %s, %S)
    """

    cur.execute(sql, (client["cookie"], client["is_user"], client["user_id"]))

    conn.commit()


def get_category_id(name: str):
    sql = """
        SELECT category_id FROM categories
        WHERE category_name = (%s)
    """

    cur.execute(sql, name)

    conn.commit()
