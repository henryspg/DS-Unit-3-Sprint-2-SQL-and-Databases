import sqlite3


def connect_to_db(db_name='rpg_db.sqlite3'):
    return sqlite3.connect(db_name)


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


GET_CHARACTERS = """
  SELECT *
  FROM charactercreator_character;
"""

# 1. How many total Characters are there?

Total_Characters = """
  SELECT count(*)  
  FROM charactercreator_character;
  """

# 2. How many of each specific subclass?


# 3. How many total Items?
Total_Item = """
    SELECT count(*)
    FROM armory_item;
    """

# 4. How many of the Items are weapons? How many are not?
Weapon = """
    SELECT count(*) FROM armory_weapon;
    """

# 4a. How many of the Items are weapons? How many are not?
Weapon_incl = """
    select count(*) from armory_item
    LEFT join armory_weapon
    ON item_id = item_ptr_id
    where item_ptr_id not NULL
    """

# 4b. How many of the Items are not weapon?
Weapon_excl = """
    select count(*) from armory_item
    LEFT join armory_weapon
    ON item_id = item_ptr_id
    where item_ptr_id is NULL
    """

# 5. How many Items does each character have? (Return first 20 rows)
char_item20 = """
        select character_id, name, count(item_id) FROM(
        SELECT cc.character_id, cc.name, ai.item_id, ai.name 
		FROM charactercreator_character as cc,
		armory_item as ai,
		charactercreator_character_inventory as cci
		WHERE cc.character_id = cci.character_id 
		AND ai.item_id = cci.item_id
		)
		GROUP BY 1 order by	3 DESC
		LIMIT 20
"""

# 6-•	How many Weapons does each character have? (Return first 20 rows)
weapon_per_character = """
SELECT character_id, count(item_id) from charactercreator_character_inventory
		join armory_weapon
		on item_id = item_ptr_id
		group by 1
		order by 2 DESC
		limit 20
"""


# 7-•	On average, how many Items does each Character have?  answer is easily seen: 5
item_character = """
SELECT character_id, name, count(item_id) FROM(
SELECT cc.character_id, cc.name, ai.item_id, ai.name 
		FROM charactercreator_character as cc,
		armory_item as ai,
		charactercreator_character_inventory as cci
		WHERE cc.character_id = cci.character_id 
		AND ai.item_id = cci.item_id
		)
		GROUP BY 1 order by	3 DESC
		LIMIT 1
"""






if __name__ == '__main__':
    conn = connect_to_db()
    curs = conn.cursor()
    result1 = execute_query(curs, GET_CHARACTERS)
    result2 = execute_query(curs, Total_Characters)
    result3 = execute_query(curs, Total_Item)
    result4a = execute_query(curs, Weapon_incl)
    result4b = execute_query(curs, Weapon_excl)
    result5 = execute_query(curs, char_item20)
    result6 = execute_query(curs, weapon_per_character)
    result7 = execute_query(curs, item_character)


    # print(result1)
    print("1-How many total Characters are there?\n",  result2)
    print("\n3-How many total Items?\n",  result3)
    # print("result3 = execute_query(curs, Total_Item)")
    print("\n4a-How many of the Items are weapons?\n", result4a )
    print("\n4b-How many are not weapons?\n", result4b)
    print("\n5-How many Items does each character have?\n", result5)
    print("\n6-How many Weapons does each character have?\n", result6)
    print("\n7-On average, how many Items does each Character have?\n", result7)

