import sqlite3


class SQLiteDatabase:
    """
    Database context manager to automatically open, commit and close db connection
    """
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


def get_all_ids():
    """
    Return all user's ids stored in db
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        ids = []
        c.execute("""
            SELECT id FROM users;
                    """)
        query = c.fetchall()
        for el in query:
            for i in el:
                ids.append(i)
        return ids


def get_ids_to_notify():
    """
    Returns all user's ids where Notification turned On
    """
    ids_to_notify = []
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""          
                SELECT id FROM main.users
                WHERE do_notify == 1;
                            """)
        query = c.fetchall()
        for el in query:
            for i in el:
                ids_to_notify.append(i)
        return ids_to_notify


def check_if_notify_user(user_id):
    """
    Checks if user's notification is turned On
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""SELECT do_notify FROM users 
                                        WHERE id == (?)""", (user_id,))
        do_notify = c.fetchall()[0][0]
        return do_notify


def delete_user(user_id):
    """
    Deletes user from db
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
                               DELETE FROM users
                               WHERE id == (?)
                           """, (user_id,))


def set_notify_on(user_id):
    """
    Turns On notifications for specific user
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
                                        UPDATE users
                                        SET do_notify = 1
                                        WHERE id == (?);
                                    """, (user_id,))


def set_notify_off(user_id):
    """
        Turns Off notifications for specific user
        """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
                                        UPDATE users
                                        SET do_notify = 0
                                        WHERE id == (?);
                                    """, (user_id,))


def update_location(user_lat, user_lng, user_id):
    """
    Updates user's coordinates + reboots last notified field to default
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
                                       UPDATE users
                                       SET lat = (?), lng = (?), last_notified = 1
                                       WHERE id == (?);
                                   """, (user_lat, user_lng, user_id))


def set_new_location(user_id, user_username, user_f_name, user_lat, user_lng):
    """
    Registers new user to db and sets its location
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
                                               INSERT INTO users (id, username, f_name, lat, lng) 
                                               VALUES (?, ?, ?, ?, ?)
                                   """, (user_id, user_username, user_f_name, user_lat, user_lng))


def get_user_coordinates_to_notify(user, current_unix_time):
    """
    Returns coordinates of a user
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
    
                               SELECT lat, lng FROM users
                               WHERE id == (?) AND last_notified < ((?) - 1800);
    
                           """, (user, current_unix_time))

        data = c.fetchall()
        return data


def set_new_last_notified(current_unix_time, user):
    """
    Updates last notified field after user notification is done
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
                                        UPDATE users
                                        SET last_notified = (?)
                                        WHERE id == (?);
                                        """, (current_unix_time, user))


def check_if_user_signed_up(user_id):
    """
    Checks if user id is registered in db
    """
    with SQLiteDatabase("database/iss_now.db") as c:
        c.execute("""
        SELECT * FROM users
        WHERE id == (?);
        """, (user_id,))
        data = c.fetchall()
        return data


if __name__ == "__main__":
    all_ids = get_all_ids()
    print(all_ids)
