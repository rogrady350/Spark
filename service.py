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

#add data sent from create-profile form into new db collection
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

        profile_collection.insert_one(data) #add JSON object to "profiles" collection
        return {"msg": "profile created successfully"}
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

#retrieve profile data from db (general purpose: logged in user or another user)
def get_profile(user_id):
    if not user_id:
        return {"error": "Unauthorized"} #handle error for no user_id provided
    
    #convert user_id, stored as Object id in Mongo
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return {"error": "Invalid User ID"}
    
    #find user profile
    user = profile_collection.find_one({"_id": user_object_id})

    if user:
        user["_id"] = str(user["_id"])
        user.pop("password", None) #remove password
        print("Retrieved user data:", user) #debug
        return user

    return {"error": "User not found"}

#retreive another profile(calls get_profile)
def get_next_profile(logged_in_user_id, last_seen_id=None):
    #must be logged in to browse profiles
    if not logged_in_user_id:
        return {"error": "Unauthorized"}
    
    #convert ObjectId from mongo
    try:
        logged_in_user_object_id = ObjectId(logged_in_user_id) 
    except Exception:
        return {"error": "Invalid User ID"}
    
    query = {"_id": {"$ne": logged_in_user_object_id}} #exclude showing personal profile

    if last_seen_id:
        try:
            last_seen_object_id = ObjectId(last_seen_id)
            query["_id"] = {"$gt": last_seen_object_id} #for now just fetch next profile in order
        except Exception:
            return {"error": "Invalid last seen id"}
        
    #find next profile to display
    next_profile = profile_collection.find_one(query, sort=[("_id", 1)])

    #use get profile method for profile retrieval
    if next_profile:
        return get_profile(next_profile["_id"])
    
    #error if user has seen all available profiles
    return {"error": "No more profiles to view"}

#update personal profile data from update-profile form (logged in user) in db
def update_info(user_id, updated_data):
    #data from form to updated. exclude fields with None values.
    # prevent overwriting currently saved info without user needing to fill out every field
    update_data = {key: value for key, value in updated_data.items() if value is not None}

    if not user_id:
        return {"error": "Unauthorized"}
    
    if not update_data:
        return {"error": "No data to update"}
    
    #convert user_id, stored as Object id in Mongo
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return {"error": "Invalid User ID"}

    #update db collection
    result = profile_collection.update_one(
        {"_id": user_object_id},
        {"$set": update_data}
    )

    if result.matched_count:
        return {"msg": "profile updated sucessfully"}
    
    return {"error": "User not found"}

#add users who have you like to their db collection
def add_liked_profile(user_id, liked_user_id):
    if not user_id or not liked_user_id:
        return{"error": "Invalid User ID"}

    try: 
        user_object_id = ObjectId(user_object_id) #convert logged in user's id
        liked_object_id = ObjectId(user_id)       #converted liked user's id
    except Exception:
        return {"error": "Invalid User ID"}
    
    #update liked user's db collection, add logged-in user to liked_users array
    result = profile_collection.update_one(
        {"_id": liked_object_id},
        {"$addToSet": {"liked_users": user_object_id}} #addToSet to prevent same user from displaying more than once
    )

    if result.modified_count:
        return {"msg": "Profile liked successfully"}
    
    return {"error": "User not found or already liked"}

#retrieve list of users from like_users column in db
def get_liked_profile(user_id):
    if not user_id:
        return {"error": "Unauthorized"} #handle error for no user_id provided
    
    #convert user_id, stored as Object id in Mongo
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return {"error": "Invalid User ID"}
    
    #retrieve liked_users column from logged-in users collection
    user = profile_collection.find_one({"_id": user_object_id}, {"liked_users": 1})

    #display empty list if user has no likes yet
    #handle if both if the column doesnt exist in the collecion or list is empty
    if "liked_users" not in user or not user["liked_users"]:
        return []
    
    #fetch only necessary files for security (name, username)
    liked_profiles = profile_collection.find(
        {"_id": {"$in": user["liked_users"]}}, 
        {"first": 1, "username": 1, "_id": 0} #exclude id automatically sent by mongo for security
    )
    
    return list(liked_profiles)
