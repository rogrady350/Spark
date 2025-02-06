from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") #db connection
db = client['spark'] #select 'spark' db
profile_collection = db['profiles'] #colection (table) to store profile data

#insert data sent from create-profile form
def add_profile(data):
    try:
        profile_collection.insert_one(data) #add JSON object to "profiles" collection
        return {"msg": "SUCCESS"}
    except Exception as e:
        return {"msg": f"Error: {e}"}
    