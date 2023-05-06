import sqlite3


def get_all_ids():
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()

    ids = []
    c.execute("""
        SELECT id FROM users;
                """)
    query = c.fetchall()
    for el in query:
        for i in el:
            ids.append(i)
    db.commit()
    db.close()
    return ids


def get_ids_to_notify():
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()

    ids_to_notify = []
    c.execute("""          
            SELECT id FROM main.users
            WHERE do_notify == 1;
                        """)
    query = c.fetchall()
    for el in query:
        for i in el:
            ids_to_notify.append(i)
    db.commit()
    db.close()
    return ids_to_notify


def check_if_notify_user(user_id):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""SELECT do_notify FROM users 
                                    WHERE id == (?)""", (user_id,))
    do_notify = c.fetchall()[0][0]
    db.commit()
    db.close()
    return do_notify


def delete_user(user_id):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""
                           DELETE FROM users
                           WHERE id == (?)
                       """, (user_id,))
    db.commit()
    db.close()


def set_notify_on(user_id):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""
                                    UPDATE users
                                    SET do_notify = 1
                                    WHERE id == (?);
                                """, (user_id,))
    db.commit()
    db.close()


def set_notify_off(user_id):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""
                                    UPDATE users
                                    SET do_notify = 0
                                    WHERE id == (?);
                                """, (user_id,))
    db.commit()
    db.close()


def update_location(user_lat, user_lng, user_id):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""
                                   UPDATE users
                                   SET lat = (?), lng = (?), last_notified = 1
                                   WHERE id == (?);
                               """, (user_lat, user_lng, user_id))
    db.commit()
    db.close()


def set_new_location(user_id, user_username, user_f_name, user_lat, user_lng):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""
                                           INSERT INTO users (id, username, f_name, lat, lng) 
                                           VALUES (?, ?, ?, ?, ?)
                               """, (user_id, user_username, user_f_name, user_lat, user_lng))
    db.commit()
    db.close()


def get_user_coordinates_to_notify(user, current_unix_time):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""

                           SELECT lat, lng FROM users
                           WHERE id == (?) AND last_notified < ((?) - 1800);

                       """, (user, current_unix_time))

    data = c.fetchall()
    db.commit()
    db.close()
    return data


def set_new_last_notified(current_unix_time, user):
    db = sqlite3.connect("database/iss_now.db")
    c = db.cursor()
    c.execute("""
                                    UPDATE users
                                    SET last_notified = (?)
                                    WHERE id == (?);
                                    """, (current_unix_time, user))
    db.commit()
    db.close()


if __name__ == "__main__":
    all_ids = get_all_ids()
    print(all_ids)
