import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as np
import itertools


# Error on the titanic from github
# url = 'https://github.com/henryspg/DS-Unit-3-Sprint-2-SQL-and-Databases/blob/master/module2-sql-for-analysis/titanic.csv'
# url = 'https://github.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/blob/master/module2-sql-for-analysis/titanic.csv'
# titanic = pd.read_csv(url, sep= '\t')

# I use titanic downloaded to my directory
titanic = pd.read_csv('titanic.csv')
titanic.columns = ['Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Pchild', 'Fare' ]

# For early check
# print(titanic.head(3))

# Credentials
dbname = 'tpeczybx'
user = 'tpeczybx'  # ElephantSQL happens to use same name for db and user
password = 'zzzzz'  
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


# TEST if the empty table is created
pg_curs.execute('SELECT * FROM titanic;')
# print("\nCheck if the empty table is created :\n" , pg_curs.fetchall())

####################################################################

# from https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table

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
# print("\nFINAL TITANIC TABLE ['Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Pchild', 'Fare']:: \n\n" , pg_curs.fetchall())

# pg_curs.close() ###


######################### The above code was from Module 2, and below code if from Module 4 ##################################
######################### The above code was from Module 2, and below code if from Module 4 ##################################



# Questions
survived = """
select count(*) from titanic
where Survived = 1;
"""

pg_curs.execute(survived)
print("\n1a-Total survived :\n" , pg_curs.fetchall()[0][0] )


died = """
select count(*) from titanic
where Survived = 0;
"""

pg_curs.execute(died)
print("\n1b Total died :\n" , pg_curs.fetchall()[0][0] )

##################################################################################

passenger_class = """
select count(*), Pclass from titanic
GROUP BY Pclass;
"""

pg_curs.execute(passenger_class)
print("\n2 Total (passenger, each_class) :\n" , pg_curs.fetchall() )
print()

# This code didnt work
# P_class = [lis[1] for lis in pg_curs.fetchall()] 
# print("\n\nPclass", P_class)



##################################################################################
surv1_class = """
select count(*), Pclass from titanic
where Survived = 1
GROUP BY Pclass;
"""

pg_curs.execute(surv1_class)
print("\n3a Total Survived(passenger, each_class) :\n" , pg_curs.fetchall() )

##################################################################################
surv0_class = """
select count(*), Pclass from titanic
where Survived = 0
GROUP BY Pclass;
"""

pg_curs.execute(surv0_class)
print("\n3b Total Died(passenger, each_class) :\n" , pg_curs.fetchall() )

##################################################################################
Age_survive = """
select avg(Age), Survived from titanic
GROUP BY Survived;
"""

pg_curs.execute(Age_survive)
print("\n4 Passengers(Age, survived/death) :\n" , pg_curs.fetchall() )

##################################################################################
Age_Pclass = """
select avg(Age), Pclass from titanic
GROUP BY Pclass;
"""

pg_curs.execute(Age_Pclass)
print("\n5 Average age of each Pclass(Age, class) :\n" , pg_curs.fetchall() )


##################################################################################
Fare_Pclass = """
select avg(Fare), Pclass from titanic
GROUP BY Pclass;
"""

pg_curs.execute(Fare_Pclass)
print("\n6a Average Fare of each Pclass(Fare, class) :\n" , pg_curs.fetchall() )

##################################################################################
Fare_Survive = """
select avg(Fare), Survived from titanic
GROUP BY Survived;
"""

pg_curs.execute(Fare_Survive)
print("\n6b Average Fare by survival(Fare, survival) :\n" , pg_curs.fetchall() )

##################################################################################
SibSp_Pclass = """
select count(SibSp), Pclass from titanic
GROUP BY Pclass;
"""

pg_curs.execute(SibSp_Pclass)
print("\n7a Sibling/Spouse by Pclass(count, Pclass) :\n" , pg_curs.fetchall() )
##################################################################################
SibSp_survival = """
select count(SibSp), Survived from titanic
GROUP BY Survived;
"""

pg_curs.execute(SibSp_survival)
print("\n7b Sibling/Spouse by survival(count, survival) :\n" , pg_curs.fetchall() )
##################################################################################
Pchild_pclass = """
select avg(Pchild), Pclass from titanic
GROUP BY Pclass;
"""

pg_curs.execute(Pchild_pclass)
print("\n8a Average parent-children by Pclass(average, pclass) :\n" , pg_curs.fetchall() )

##################################################################################
Pchild_survival = """
select avg(Pchild), Survived from titanic
GROUP BY Survived;
"""

pg_curs.execute(Pchild_survival)
print("\n8b Average parent-children by survival(average, survival) :\n" , pg_curs.fetchall() )

##################################################################################
same_name = """
select count(Name) - count (distinct Name) from titanic

"""

pg_curs.execute(same_name)
print("\n9 How many passangers have the same name? :\n" , pg_curs.fetchall() )
##################################################################################
print("\n10 In the list, not all married couple have the same last names.\n   just like: Cumings, Samaan... etc\n")
##################################################################################

##################################################################################


pg_conn.commit()
pg_curs.close() ###
