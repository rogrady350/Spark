#score weighted filtering methods
from service import get_profile, profile_collection
from bson import ObjectId
import numpy as np #library for numerical computing

#Normalize fields - adds default null values so empty fields don't cause crash
DEFAULT_PROFILE_FIELDS = {
    "politics": None,
    "religion": None,
    "wantChildren": None,
    "haveChildren": None,
    "matchPreferences": [],
    "gender": None,
    "age": None,
    "skipped_users": [],
    "matched_users": [],
    "liked_users": [],
}

#should add drinking/smoking options

#Value lists for One Hot Encoding - convert categorical variables into binary
GENDER_OPTIONS = ["male", "female", "nonbinary", "transgender"]
POLITICS_OPTIONS = ["liberal", "moderate", "conservative"]
RELIGION_OPTIONS = ["christian", "jewish", "muslim", "catholic", "atheist"]
FAMILY_OPTIONS = ["want", "open", "unsure", "dont"]

#Helper to build One Hot vectors. Assign index of option to vector
def one_hot(value, options):
    vector = []
    if value not in options:
        return None #skip "other" and "prefer not to say" in scoring

    for option in options:
        if value == option:
            vector.append(1)
        else:
            vector.append(0)

    return vector

#Helper function for yes/no style questions (currently only haveChildren)
def encode_boolean(value):
    if value == "yes":
        return 1
    elif value == "no":
        return 0
    else:
        return None #skip prefer not to say (or possibly an other in the furture) in scoring
    
#Helper function to create vector for a profile
def profile_vector(profile):
    try:
        age = int(profile.get("age", 0))
    except:
        age = 0 #fall back for not possible age

    #normalize age (assume max age of 100)
    #ML algorithms work better when features are scaled - prevents large values from dominating
    normalized_age = age/100

    #vector encoding
    #boolean: empty string if not filled out. 1 for have, 0 for don't, none for prefer not to say
    have_children = encode_boolean(profile.get("haveChildren", ""), ["yes"]) 

    #one_hot: empty string if not filled out. vector corresponding to response value
    gender_vec = one_hot(profile.get("gender", ""), GENDER_OPTIONS)
    politics_vec = one_hot(profile.get("politics", ""), POLITICS_OPTIONS)
    religion_vec = one_hot(profile.get("religion", ""), RELIGION_OPTIONS)
    family_vec = one_hot(profile.get("wantChildren", ""), FAMILY_OPTIONS)

    #NumPy vector - gives you: fast math operations, shape control, numerical compatibility with ML models (cosine similarity)
    #group scalars (age, booleans) and concatenate lists (one hot vectors) into one list
    #ndarray - faster and more powerful list. supporsts multidimensial arrays. apply math to arrays without needing for loops
    return np.array([normalized_age], have_children) +\
          gender_vec +\
          politics_vec +\
          religion_vec +\
          family_vec

#determine cosine similarity - how close candidate user is to logged in user
def cosine_similarity(profile1_vec, profile2_vec):
    if profile1_vec is None or profile2_vec is None:
        return 0
    
    #vectors MUST be sent as NumPy arrays to calculate dot products.
    #profile_vector method returns np.array's
    dot_product = np.dot(profile1_vec, profile2_vec)

    #normalize vectors - calculate length (magnitude) of each vector
    norm_profile1_vec = np.linalg.norm(profile1_vec)
    norm_profile2_vec = np.linalg.norm(profile2_vec)

    #safety check for a vector of zero - prevent divide by 0 exception
    if norm_profile1_vec == 0 or norm_profile2_vec == 0:
        return 0 #set similarity to 0
    
    #caluclate and return cosine similarity of 2 profiles - run formula
    return dot_product / (norm_profile1_vec * norm_profile2_vec)

#Helper function to normalize profiles
def normalize_profile(profile):
    for field, default in DEFAULT_PROFILE_FIELDS.items():
        #if field exists return the value (field), otherwise retrun null (defualt value)
        profile[field] = profile.get(field, default)
    return profile

#calculate level of compatability
def calculate_compatibility(user, recommended_user):
    score = 0 #set score to 0 initially

    #increase score for closer age
    #absolute value to always get positive difference. cast to int to prevent crash from bad front end data. (need to update front end to store as int.)
    age_difference = abs(int(user["age"]) - int(recommended_user["age"])) 
    if age_difference < 3:
        score += 3
    elif age_difference < 7:
        score += 2
    elif age_difference < 10:
        score += 1

    #increase score for shared preferences
    if user["politics"] == recommended_user["politics"]:
        score += 2
    if user["religion"] == recommended_user["religion"]:
        score += 2
    if user["wantChildren"] == recommended_user["wantChildren"]:
        score += 2

    return score

#use score to return list of recommendations
def get_ranked_recommendations(user_id):
    #debug
    print(f"grr Running recommendation logic for user ID: {user_id}")

    user = get_profile(user_id, include_arrays=True)
    if "error" in user:
        print("ERROR: User profile not found.")
        return []
    
    user = normalize_profile(user) #normalize after profile data retrieved

    #do not show skipped, matched, and viewed profiles. #if any are none, fall back to empty list
    #convert ObjectId from lists to string and store in set of unique uid's
    #skipped and matched list stored under current user-id collection
    skipped = [str(uid) for uid in user.get("skipped_users", [])]
    matched = [str(uid) for uid in user.get("matched_users", [])]

    #find users who were liked by the current user (where current user-id appears in others liked_users collection)
    liked_cursor = profile_collection.find(
        {"liked_users": ObjectId(user_id)},
        {"_id": 1}
    )
    liked = [str(profile["_id"]) for profile in liked_cursor]

    #build viewed set
    viewed = set(skipped + liked + matched)

    candidates_list = list(profile_collection.find({"_id": {"$ne": ObjectId(user_id)}}))
    #debug if pulling all users from db
    print("grr Total candidates returned from DB:", len(candidates_list))

    # Remove password from all candidates early
    for candidate in candidates_list:
        candidate.pop("password", None)
        candidate.pop("skipped_users", None)
        candidate.pop("matched_users", None)
        candidate.pop("liked_users", None)

    #create list of tuples of scored candiate users with their compatability score
    scored_candidates = []

    for c in candidates_list:
        c = normalize_profile(c) #normalize candidate before filtering
        #filter viewed
        if str(c["_id"]) in viewed:
            continue

        #only display recommended candidate if user and candidates matchPreferences are both satisfied by the other
        #filter desired gender matches of user
        if user.get("matchPreferences") and c.get("gender") not in user["matchPreferences"]:
            continue
        #filter desired gender matches of candidate users to user
        if c.get("matchPreferences") and user.get("gender") not in c["matchPreferences"]:
            continue

        #calculated compatibility of filtered list of users
        score = calculate_compatibility(user, c)

        #only append users with some compatability (score > 0)
        if score > 0:
            c["_id"] = str(c["_id"]) #convert ObjectId to string (for JSON serializaztion in frontend)
            scored_candidates.append((c,score))  #append 1 (profile, score) tuple per match

    #sort candidates by score. anonymous lambda function gets score (second element) from list, highest ranked first
    scored_candidates.sort(key=lambda x: x[1], reverse=True)

    #print to verify candidate and rank are displaying accurate results
    print("grr Ranked Recommendations:\n")
    for rank, (candidate, score) in enumerate(scored_candidates, start=1): #get tuple from list
        print(f"grr Rankd {rank}: {candidate['username']} (Score): {score})")  #print candidate username and their rank

    #extract candidate profile (c) from linked list and return list of recommended users
    return [c for c, s in scored_candidates]

#retreive next recommended profile - updated with filtering logic from recommendations.py
def get_next_profile(logged_in_user_id, last_seen_id=None):
    #must be logged in to browse profiles
    if not logged_in_user_id:
        return {"error": "Unauthorized"}
    
    #get list of recommendations
    try:
        #call function to generate list of of recommended users for logged in user
        recommendations = get_ranked_recommendations(logged_in_user_id)
    except Exception as e:
        return {"error": f"Failed to generate recommendations: {e}"}
    
    #show first profile in list on load (no last_seen_id)
    if not last_seen_id:
        #return first recommendation (only if recommendations is not empty)
        if recommendations:
            return recommendations[0]
    #after first recommendation return next in list
    else:
        #increment to next profile to display
        #enumerate is cleaner to use since current index and item are both need. avoid having to manage counter manually
        for i, profile in enumerate(recommendations):
            #display next profile if there are more left to display
            if profile["_id"] == last_seen_id and i+1 < len(recommendations):
                return recommendations[i+1]
            
        print("grr last_seen_id not found in recommendations. Showing first available.")
        if recommendations:
            return recommendations[0]
            
    #return message once all profiles have been viewed
    return {"msg": "No more profiles to view"}