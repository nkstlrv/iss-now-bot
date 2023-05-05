import sqlite3


def get_all_ids():
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
    db.close()

    return ids


def get_ids_to_notify():
    db = sqlite3.connect("data/iss_now.db")
    c = db.cursor()

    ids_to_notify = []

    c.execute("""
                SELECT id FROM config
                WHERE do_notify == 1;
            """)

    query = c.fetchall()

    for el in query:
        for i in el:
            ids_to_notify.append(i)

    db.close()

    return ids_to_notify


if __name__ == "__main__":
    print(get_all_ids())
    print(get_ids_to_notify())
