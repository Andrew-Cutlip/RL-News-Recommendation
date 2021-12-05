# import pymongo
import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    DATABASE_URL = """
    postgres://kcdbtosywnhzwu:045c2b9d4f9833e8957004d134a20d8606129746449d8825755e5ae56dd33359@ec2-34-197-181-65.compute-1.amazonaws.com:5432/dr45l95vrdjb9
"""

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()
# noinspection SqlNoDataSourceInspection
tables = [
    """
    CREATE TABLE IF NOT EXISTS categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(255) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sources ( 
        source_id SERIAL PRIMARY KEY NOT NULL,
        source_name VARCHAR(255) NOT NULL
    );
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
        FOREIGN KEY (source_id) 
            REFERENCES sources (source_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS users ( 
        user_id SERIAL PRIMARY KEY,
        password_hash BYTEA NOT NULL,
        age INTEGER NOT NULL,
        gender VARCHAR(255) NOT NULL,
        general_rate INT NOT NULL,
        business_rate INT NOT NULL,
        entertainment_rate INT NOT NULL,
        health_rate INT NOT NULL,
        science_rate INT NOT NULL,
        sports_rate INT NOT NULL
    );
    """,
    """
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            cookie VARCHAR(255) NOT NULL,
            is_user BOOLEAN NOT NULL,
            user_id INTEGER,  
            FOREIGN KEY (user_id) 
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        );
    """,
    """
    CREATE TABLE IF NOT EXISTS clicks (
        click_id SERIAL PRIMARY KEY NOT NULL,
        art_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        clicked BOOLEAN NOT NULL,
        rated BOOLEAN NOT NULL,
        rating INTEGER,
        FOREIGN KEY (art_id) 
            REFERENCES articles (art_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (client_id)
            REFERENCES clients (client_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    );
    """
]


def create_tables(ts):
    print("Creating tables!\n")
    for table in ts:
        print(table)
        cur.execute(table)

    conn.commit()


def insert_click(click: dict):
    # need to insert a click with client id , article id
    sql = """ INSERT INTO clicks
    VALUES (%s, %s)
    """
    cur.execute(sql, (click["client_id"], click["art_id"]))

    conn.commit()


def set_click(art_id: int, client_id: int):
    sql = """
        UPDATE clicks
        SET clicked = True
        WHERE art_id = (%s) AND client_id = (%s)
    """

    cur.execute(sql, (art_id, client_id))

    conn.commit()


def set_rating(rating: int, art_id: int, client_id: int):
    sql = """
        UPDATE clicks
        SET rating = (%s)
        WHERE art_id = (%s) AND client_id = (%s)
    """

    cur.execute(sql, (rating, art_id, client_id))

    conn.commit()


def get_user_clicks(client_id: int):
    sql = """
        SELECT * FROM clicks
        WHERE client_id = (%s)
    """

    cur.execute(sql, client_id)

    conn.commit()

    rows = cur.fetchall()
    return rows


def insert_articles(articles: list):
    sql = """
        INSERT INTO articles
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for article in articles:
        cur.execute(sql,
                    (article["category_id"], article["source_id"],
                     article["author"], article["title"], article["description"],
                     article["content"], article["url"])
                    )

    conn.commit()


def insert_client(client: dict):
    sql = """
        INSERT INTO clients(cookie, is_user)
        VALUES (%s, %s)
    """
    if client["user_id"] != -1:
        print(client)
        c_id = client["user_id"]
        sql = """
            INSERT INTO clients(cookie, is_user, user_id)
            VALUES (%s, %s, %s)
        """
        cur.execute(sql, (client["cookie"], client["is_user"], c_id))
    else:
        cur.execute(sql, (client["cookie"], client["is_user"]))

    conn.commit()


def register_client(user_id: int):
    sql = """
        UPDATE clients
        SET is_user = True
        SET user_id = (%s)
    """

    cur.execute(sql, user_id)


def insert_user(user: dict):
    sql = """
        INSERT INTO users
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING user_id
    """

    cur.execute(sql, (user["password"], user["age"],
                      user["gender"], user["g"],
                      user["b"], user["e"], user["h"],
                      user["sc"], user["sp"]))

    conn.commit()

    id = conn.fetchone()[0]

    return id


def get_client_by_cookie(cookie: str):
    sql = """
                SELECT * FROM clients
                WHERE cookie = (%s)
            """

    cur.execute(sql, cookie)

    conn.commit()

    row = cur.fetchone()
    return row


def get_article_by_id(article_id: int):
    sql = """
            SELECT * FROM articles
            WHERE art_id = (%s)
        """

    cur.execute(sql, article_id)

    conn.commit()

    row = cur.fetchone()
    return row


def insert_category(name: str):
    sql = """
        INSERT INTO categories
        VALUES (%s)
    """

    cur.execute(sql, name)

    conn.commit()


def get_all_categories():
    sql = """
        SELECT name FROM categories
    """

    cur.execute(sql)

    conn.commit()

    rows = cur.fetchall()
    return rows


def get_category_id(name: str):
    sql = """
        SELECT category_id FROM categories
        WHERE category_name = (%s)
    """

    cur.execute(sql, name)

    conn.commit()

    row = cur.fetchone()
    return row


def get_source_id(name: str):
    sql = """
            SELECT source_id FROM categories
            WHERE source_name = (%s)
        """

    cur.execute(sql, name)

    conn.commit()

    row = cur.fetchone()
    return row


def insert_sources(sources: list):
    sql = """
        INSERT INTO sources(source_name)
        VALUES (%s)
    """
    for source in sources:
        print(source)
        cur.execute(sql, (source, ))

    conn.commit()


if __name__ == "__main__":
    pass
