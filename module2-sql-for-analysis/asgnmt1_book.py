# Step 1 - have the library psycopg2 installed. done

import psycopg2


# Credential:
dbname = 'tpeczybx'
user = 'tpeczybx'  
password = 'hehehe...'  
host = 'isilo.db.elephantsql.com'


# Connect to pg
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)

# Cursor
pg_curs = pg_conn.cursor()

# Creating table: book
create_table1 = """
DROP TABLE IF EXISTS books;
CREATE TABLE books (  
  book_id serial NOT NULL,
  data jsonb
);
"""
# NOTE - these types are PostgreSQL specific. This won't work in SQLite!

pg_curs.execute(create_table1)
pg_conn.commit()  # "Save" by committing


# What is in the db
pg_curs.execute('SELECT * FROM books;')
pg_curs.fetchall()

# Inserting data
insert1 = """
INSERT INTO books VALUES (1, '{"title": "Sleeping Beauties", "genres": ["Fiction", "Thriller", "Horror"], "published": false}');  
INSERT INTO books VALUES (2, '{"title": "Influence", "genres": ["Marketing & Sales", "Self-Help ", "Psychology"], "published": true}');  
INSERT INTO books VALUES (3, '{"title": "The Dictator''s Handbook", "genres": ["Law", "Politics"], "authors": ["Bruce Bueno de Mesquita", "Alastair Smith"], "published": true}');  
INSERT INTO books VALUES (4, '{"title": "Deep Work", "genres": ["Productivity", "Reference"], "published": true}');  
INSERT INTO books VALUES (5, '{"title": "Siddhartha", "genres": ["Fiction", "Spirituality"], "published": true}');  
"""

# Execute & Commit
pg_curs.execute(insert1)

# "Save" by committing
pg_conn.commit()


pg_curs.execute('SELECT * FROM test_table;')
pg_curs.fetchall()

# Close if we r done
pg_curs.close()



# Ensure data quality
# Note: the data shuld not be NULLS, as mentioned above
pg_curs = pg_conn.cursor()
pg_curs.execute('INSERT INTO books (data) VALUES (null);');