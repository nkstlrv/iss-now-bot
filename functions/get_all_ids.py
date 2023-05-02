import sqlite3


def get_ids():
    db = sqlite3.connect('data/iss_now.db')
    c = db.cursor()

    ids = []

    c.execute("""
            SELECT id FROM config;
        """)

    query = c.fetchall()

    for el in query:
        for i in el:
            ids.append(i)

    return ids


if __name__ == "__main__":
    print(get_ids())
