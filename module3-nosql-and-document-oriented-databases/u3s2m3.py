import pymongo

print("\npymongo-version: \n", pymongo.version)
from pymongo import MongoClient


client = pymongo.MongoClient("mongodb+srv://henrylsmdb:passwd@cluster0.w8jv6.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

# Note:  dnspython was installed 
###########################################################
# A. 1st WAY - based on LECTURE.

rpg_character = (1, "Henry", "600K", 3, 'Data Scientist', 0, 0, 0)

db.test.insert_one({'rpg_character': rpg_character})

db.test.insert_one({'rpg_character': 3})
db.test.insert_one({'rpg_character': rpg_character})

rpg_doc = {
    'ID': rpg_character[0],
    'name': rpg_character[1],
    'salary': rpg_character[2],
    'level': rpg_character[3],
    'position': rpg_character[4]
}

###########################################################

# B. 2nd (BROKEN'S) WAY.
# number of elements in the rpg_character must match the rpg_doc 

# rpg_character = (1, "Henry", "600K", 3, 'Data Scientist')

# db.test.insert_one({'rpg_character': 3})
# db.test.insert_one({'rpg_character': rpg_character})

# class rpg_char:
#     id, name, salary, level, position = rpg_character

# rpg_doc ={
#     'key' : rpg_char.id,
#     'name': rpg_char.name,
#     'salary': rpg_char.salary,
#     'level' : rpg_char.level,
#     'position': rpg_char.position
# }

###########################################################

db.test.insert_one(rpg_doc)
print("\nThis is RPG_DOC:\n", rpg_doc)

db.test.find_one(rpg_doc)