from pymongo import MongoClient
import bcrypt #password-hasing library to store passwords

client = MongoClient("mongodb://localhost:27017/") #db connection
db = client['spark']                               #select 'spark' db
profile_collection = db['profiles']                #colection (table) to store profile data

#hash password, generate and add salt (random data), store hash as a string
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#check if profile with email or username already existing in db
def user_exists(email, username):
    return profile_collection.find_one({"$or": [{"email": email}, {"username": username}]}) is not None

#insert data sent from create-profile form
def add_profile(data):
    try:
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        #make sure email, username, pw is entered
        if not email or not username or not password:
            return{"msg": "Error: Email, username and password are required"}

        #check if username or email already used
        if user_exists(email, username):
            return {"msg": "Error: email or username already taken"}
        
        #hash user entered plaintext pw before storing
        data["password"] = hash_password(password)

        #add JSON object to "profiles" collection
        profile_collection.insert_one(data)
        return {"msg": "SUCCESS"}
    except Exception as e:
        return {"msg": f"Error: {e}"}
    
#verify password for login
def verify_password(username, password):
    user = profile_collection.find_one({"username:": username})

    if user:
        stored_password = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return {"msg": "Login Successful"}
        else:
            return {"msg": "Incorrect username or passord entered"}
    else:
        return {"msg": "Incorrect username or password entered"}