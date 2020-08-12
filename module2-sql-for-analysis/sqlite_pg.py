
# Step 1 - Extract, get data out of SQLite3
# charactercreator_character
import sqlite3
import psycopg2

# credentials
dbname = 'tpeczybx'
user = 'tpeczybx'  # ElephantSQL happens to use same name for db and user
password = 'hehehe...'  
host = 'isilo.db.elephantsql.com'

# cursors and connections
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)

pg_curs = pg_conn.cursor()  # Works the same as SQLite!


sl_conn = sqlite3.connect('rpg_db.sqlite3')

sl_curs = sl_conn.cursor()

get_characters = "SELECT * FROM charactercreator_character;"
sl_curs.execute(get_characters)
characters = sl_curs.fetchall()

# Test: length = 302?
print("length of characters = \n", len(characters))


print("\ncharacters[:3] :\n", characters[:3])


# Step 2 - Transform
sl_curs.execute('PRAGMA table_info(charactercreator_character);')
print("\nsl_curs.fetchall \n",   sl_curs.fetchall())


# Create statement for PostgreSQL:
create_character_table = """
DROP TABLE IF EXISTS charactercreator_character;
CREATE TABLE charactercreator_character (
  character_id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  level INT,
  exp INT,
  hp INT,
  strength INT,
  intelligence INT,
  dexterity INT,
  wisdom INT
);
"""


# Defining a function to refresh connection and cursor
def refresh_connection_and_cursor(conn, curs):
    curs.close()
    conn.close()
    pg_conn = psycopg2.connect(dbname=dbname, user=user,
                             password=password, host=host)
    pg_curs = pg_conn.cursor()
    return pg_conn, pg_curs



pg_conn, pg_curs = refresh_connection_and_cursor(pg_conn, pg_curs)

# Execute the create table
pg_curs.execute(create_character_table)
pg_conn.commit()


# PostgreSQL comparison to the SQLite pragma
# This is showing postgresql internals
show_tables = """
SELECT
   *
FROM
   pg_catalog.pg_tables
WHERE
   schemaname != 'pg_catalog'
AND schemaname != 'information_schema';
"""



pg_curs.execute(show_tables)
print("\npg_curs.fetchall :\n",  pg_curs.fetchall())


# Test characters[0]
print("\ncharacters[0]  :\n", characters[0])


# INSERT data (for inspection)
example_insert = """
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES """ + str(characters[0][1:]) + ";"

print(example_insert)  # Not running, just inspecting


# Execute each character one at a time
for character in characters:
    insert_character = """
    INSERT INTO charactercreator_character
    (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
    VALUES """ + str(character[1:]) + ";"
    pg_curs.execute(insert_character)

# commit
pg_conn.commit()


# Show the data
pg_curs.execute('SELECT * FROM charactercreator_character LIMIT 3;')
print("\npg_curs.fetchall_character : \n" , pg_curs.fetchall())


# Check sustematically
pg_curs.execute('SELECT * FROM charactercreator_character;')
pg_characters = pg_curs.fetchall()


# Test again -assert
# No error means they're all the same!, 
for character, pg_character in zip(characters, pg_characters):
    assert character == pg_character


# Closing out cursor/connection to wrap up
pg_curs.close()
pg_conn.close()
sl_curs.close()
sl_conn.close()
