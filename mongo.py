import pymongo
from pymongo import MongoClient

# set up init cluster
cluster = MongoClient("mongodb+srv://adminTyler:paWoodHJ9qohPLDs@cluster0.nce7s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# select database
db = cluster["inChest"]
# select user collection
collection = db["level"]

# data to insert to user collection
# post = {"_id": 0, "fname": 'Tyler', 'lname': 'Nguyen'}
# collection.insert_one(post)

# insert a level
# level = {"_id": 0, "level": 'easy'}
# collection.insert_one(level)

# this will find all the data from level collection
result = collection.find({})

for x in result:
    print(x)
