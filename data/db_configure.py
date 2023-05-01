import sqlite3


def configure_db():
    print('Creating Database...')
    db = sqlite3.connect('iss_now.db')
    print('Database created')

    c = db.cursor()
    c.execute("""CREATE TABLE UserConfig(
        
        id int NOT NULL UNIQUE PRIMARY KEY ,
        username varchar(250) NOT NULL,
        f_name varchar(255) NOT NULL DEFAULT 'no name',
        notify boolean not null default false

    );""")

    c.execute("""
        INSERT INTO UserConfig (id, username, f_name) 
        VALUES (0, 'test', 'test');
    """)

    db.close()
    print('DB Closed')


if __name__ == "__main__":
    # configure_db()
    pass
