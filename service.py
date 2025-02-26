from pymongo import MongoClient
from bson import ObjectId
import bcrypt #password-hasing library to store passwords

client = MongoClient("mongodb://localhost:27017/") #db connection
db = client['spark']                               #select 'spark' db
profile_collection = db['profiles']                #colection (table) to store profile data

#hash password, generate and add salt (random data), stored as bytes
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#check if profile with email or username already existing in db
def user_exists(email, username):
    return profile_collection.find_one({"$or": [{"email": email}, {"username": username}]}) is not None

#insert data sent from create-profile form int db
def add_profile(data):
    try:
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        #make sure email, username, pw is entered
        if not email or not username or not password:
            return{"msg": "Error: Email, username and password are required"}

        #check if username or email already used
        if user_exists(email, username):
            return {"msg": "Error: email or username already taken"}
        
        #hash user entered plaintext pw before storing
        data["password"] = hash_password(password)

        profile_template = {
            #fileds required for account creation
            "username": username,
            "password": data["password"],
            "email": email,
            "first": data.get("first"),
            "last": data.get("last"),
            "age": data.get("age"),

            #additional information fields left blank on creation
            "occupation": data.get(None),
            "gender": data.get(None),
            "matchPreferences": data.get(None),
            "politics": data.get(None),
            "religion": data.get(None),
            "wantChildren": data.get(None),
            "haveChildren": data.get(None)
        }

        profile_collection.insert_one(data) #add JSON object to "profiles" collection
        return {"msg": "SUCCESS"}
    except Exception as e:
        return {"msg": f"Error: {e}"}
    
#verify password for login
def verify_password(username, password):
    user = profile_collection.find_one({"username": username}) #find user with entered username in db

    if user:
        stored_password = user["password"] #get hashed password for user from db
        if bcrypt.checkpw(password.encode('utf-8'), stored_password): #encode entered plaintext pw and compare to stored pw
            return {"success": True, "user_id": str(user["_id"]), "msg": "Login Successful"} #return Mongo's ObjectId as a string if correct pw entered
        else:
            return {"success": False, "msg": "Incorrect username or password"} #return false for inccorect pw entered
    else:
        return {"success": False, "msg": "Incorrect username or password"} #return false for username not in db

#retrieve personal profile data (logged in user) from db
def get_profile(user_id):
    if not user_id:
        return {"error": "Unauthorized"} #handle error for no user_id provided
    
    try:
        user_object_id = ObjectId(user_id) #convert user_id, stored as Object id in Mongo
    except Exception:
        return {"error": "Invalid User ID"}
    
    user = profile_collection.find_one(
        {"_id": user_object_id}, #find user matching this id
        {"_id": 0, "username": 1, "first": 1, "last": 1, "email": 1, "age": 1} #return values from db with 1
    )

    if not user:
        return {"error": "User not found"}
    
    return user 