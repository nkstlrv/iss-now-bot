import sqlite3


def configure_db():
    print('Creating Database...')
    db = sqlite3.connect('iss_now.db')
    print('Database created')

    c = db.cursor()
    c.execute("""CREATE TABLE config(
        
        id int NOT NULL UNIQUE PRIMARY KEY ,
        username text NOT NULL,
        f_name text NOT NULL DEFAULT 'no name',
        lat real default null,
        lng real default null,
        do_notify boolean not null default false,
        last_notified integer default Null
        
        
    );""")

    db.commit()

    db.close()
    print('DB Closed')


if __name__ == "__main__":
    configure_db()


