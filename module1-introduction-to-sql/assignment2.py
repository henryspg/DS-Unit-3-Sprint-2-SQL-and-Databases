import sqlite3
import pandas as pd


def connect_to_db(db_name='buddymove_holidayiq.sqlite3'):
    return sqlite3.connect(db_name)


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()



df = pd.read_csv('buddymove_holidayiq.csv')



GET_ALL= """
  SELECT *
  FROM reviews;
"""
conn = connect_to_db('buddymove_holidayiq.sqlite3')
curs = conn.cursor()

def put_reviews_in_db():
  
    curs.execute("DROP TABLE reviews")
    df.to_sql('reviews', conn)


put_reviews_in_db()





# a = execute_query(curs, GET_ALL)

# 1-How many rows?
Total_rows = """
select count(*) from reviews
"""

# 2-users reviewed >=100 Nature also reviewed >=100 in the Shopping
review100 = """
select count(*) from reviews
where Nature >=100 AND Shopping >=100
"""

# 3-strech - average of each category
avg_cat = """
select  avg(Sports), avg(Religious), avg(Nature), avg(Theatre), avg(Shopping), avg(Picnic) from reviews
"""



if __name__ == '__main__':
    conn = connect_to_db()
    curs = conn.cursor()
    test_to_see_database = execute_query(curs, GET_ALL)
    # print("get all at the beginning: ", test_to_see_database)
    # result1 = execute_query(curs, GET_CHARACTERS)
    result1 = execute_query(curs, Total_rows)
    result2 = execute_query(curs, review100)
    result3 = execute_query(curs, avg_cat)


    # # print(result1)
    print("1-How many rows?\n",  result1)
    print("\n2-users reviewed >=100 Nature also reviewed >=100 in the Shopping\n",  result2)
    print("\n3-average per category", result3)
 