#score weighted filtering methods
from service import get_profile, profile_collection
from bson import ObjectId

#calculate level of compatability
def calculate_compatibility(user, recommended_user):
    score = 0 #set score to 0 initially

    #increase score for closer age
    #absolute value to always get positive difference. cast to int to prevent crash from bad front end data. (need to update front end to store as int.)
    age_difference = abs(int(user["age"]) - int(recommended_user["age"])) 
    #age debug
    print(f"Scoring: {user.get('username')} vs {recommended_user.get('username')}")
    print(f"User age: {user.get('age')}, Candidate age: {recommended_user.get('age')}")
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

    user = get_profile(user_id)
    if "error" in user:
        print("ERROR: User profile not found.")
        return []

    print(f"grr Retrieved user data: {user}")
    print(f"grr User match prefs: {user.get('matchPreferences')}, gender: {user.get('gender')}")

    #do not show skipped, matched, and viewed profiles
    #if either liked or matched is none, fall back to empty list
    skipped = user.get("liked_users") or []
    matched = user.get("matched_profiles") or []
    
    #convert ObjectId from skipped and matched list to string and store in set of unique uid's
    viewed = set(str(uid) for uid in skipped + matched)

    candidates_list = list(profile_collection.find({"_id": {"$ne": ObjectId(user_id)}}))
    #debug if pulling all users from db
    print("grr Total candidates returned from DB:", len(candidates_list))

    # Remove password from all candidates early
    for candidate in candidates_list:
        candidate.pop("password", None)

    #create list of tuples of scored candiate users with their compatability score
    scored_candidates = []

    for c in candidates_list:
        #filter viewed
        if str(c["_id"]) in viewed:
            print(f"Skipping {c['username']} (already viewed)")
            continue
        #filter desired gender matches of user
        #if user.get("matchPreferences") and c.get("gender") not in user["matchPreferences"]:
        #    print(f"Skipping {c['username']} | Candidate: {c['username']} gender: {c.get('gender')} (gender mismatch)")
        #    continue
        #filter desired gender matches of candidate users to user
        #if c.get("matchPreferences") and user.get("gender") not in c["matchPreferences"]:
        #    print(f"Skipping {c['username']} (candidate doesn't match with user gender)")
        #    continue

        #calculated compatibility of filtered list of users
        print(f"grr Scoring {c['username']}")
        score = calculate_compatibility(user, c)
        print(f"grr Score for {c['username']}: {score}")

        #only append users with some compatability (score > 0)
        if score > 0:
            print(f"grr Score for {c['username']}: {score}")
            c["_id"] = str(c["_id"]) #convert ObjectId to string (for JSON serializaztion in frontend)
            scored_candidates.append((c,score))  #append 1 (profile, score) tuple per match

    #debug users added to recommendation list
    print("grr Final scored candidates:", [c[0]['username'] for c in scored_candidates])

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
            
    #return message once all profiles have been viewed
    return {"msg": "No more profiles to view"}