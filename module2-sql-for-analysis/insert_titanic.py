import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as np
# import sql 


# Error on the titanic from github
# url = 'https://github.com/henryspg/DS-Unit-3-Sprint-2-SQL-and-Databases/blob/master/module2-sql-for-analysis/titanic2.csv'
# titanic = pd.read_csv(url)

# I use titanic downloaded to my directory
titanic = pd.read_csv('titanic.csv')
titanic.columns = ['Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Pchild', 'Fare' ]

# For early check
print(titanic.head(3))

# Credentials
dbname = 'tpeczybx'
user = 'tpeczybx'  # ElephantSQL happens to use same name for db and user
password = 'hehehe...'  
host = 'isilo.db.elephantsql.com'


# cursors and connections
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)

pg_curs = pg_conn.cursor()


# Create table
create_table1 = """
DROP TABLE IF EXISTS titanic;
CREATE TABLE titanic (  
    Survived  INT8,
    Pclass  INT8,
    Name   varchar(120),
    Sex    varchar(10),
    Age    INT8,
    SibSp  INT8,
    Pchild INT8,
    Fare   FLOAT

);
"""

pg_curs.execute(create_table1)
pg_conn.commit()


# Check what is in the db
pg_curs.execute('SELECT * FROM titanic;')
print("\nCheck if the empty table is created :\n" , pg_curs.fetchall())

# COPY FILE didnt work though.  Hugh... :-( 
# copy_file = """
# COPY titanic FROM 'C:/MyLearning/23-LSDS/03B-LSDS17 Unit3/SQL/DS-Unit-3-Sprint-2-SQL-and-Databases/u3s2m2/titanic.csv' DELIMITER ',' CSV HEADER;
# """
# pg_curs.execute(copy_file)


####################################################################

# from https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table

print("About to insert the table .......")

df_columns = list(titanic)
# create (col1,col2,...)
columns = ",".join(df_columns)

# create VALUES('%s', '%s",...) one '%s' per column
values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

#create INSERT INTO table (columns) VALUES('%s',...)
insert_stmt = "INSERT INTO {} ({}) {}".format("titanic",columns,values)

# cur = conn.cursor()
psycopg2.extras.execute_batch(pg_curs, insert_stmt, titanic.values)

######################### below this line is from the lecture ##################################

pg_conn.commit()

pg_curs.execute('SELECT * FROM titanic;')
print("\nFINAL TITANIC TABLE ['Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Pchild', 'Fare']:: \n\n" , pg_curs.fetchall())

pg_curs.close() ###
















