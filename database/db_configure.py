import sqlite3


def configure_db():
    print('Creating Database...')
    db = sqlite3.connect('iss_now.db')
    print('Database created')

    c = db.cursor()
    c.execute("""CREATE TABLE users(
        
        id int NOT NULL UNIQUE PRIMARY KEY ,
        username text default NULL,
        f_name text NOT NULL DEFAULT NULL,
        lat real default null,
        lng real default null,
        do_notify boolean not null default false,
        last_notified integer default 1
        
        
    );""")

    db.commit()

    db.close()
    print('DB Closed')


if __name__ == "__main__":
    configure_db()


