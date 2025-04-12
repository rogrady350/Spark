from flask import render_template, request, jsonify
from service import add_match, add_profile, get_liked_profile, remove_like, verify_password, get_profile, update_info, add_liked_profile, add_skipped_profile
from recommendations import get_next_profile

def init_routes(app):
    #routes to pages
    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/create-account")
    def create_account():
        return render_template("create-account.html")
    
    @app.route("/view-profile")
    def view_profile():
        return render_template("view-profile.html")
    
    @app.route("/update-profile")
    def update_profile():
        return render_template("update-profile.html")
    
    @app.route("/view-recommendations")
    def view_recommendations():
        return render_template("view-recommendations.html")
    
    @app.route("/view-likes")
    def view_likes():
        return render_template("view-likes.html")
    
    @app.route("/view-matches")
    def view_matches():
        return render_template("view-matches.html")
    
    @app.route("/view-liked-profile")
    def view_likded_profile():
        return render_template("view-liked-profile.html")
    
    #API routes for crud operations (handle front end requests)
    #POST method for submitting data to db, server side create-account form
    @app.route("/api/create-account", methods=["POST"])
    def create_account_api():
        data = request.get_json() #get JSON data from request body
        result = add_profile(data) #call function to insert into MongoDB
        
        if "Error" in result["msg"]:
            return jsonify(result), 400  #HTTP 400 (Bad Request) for errors
        
        return jsonify(result), 201 #HTTP 201 (Created) for successful profile creations
    
    #POST method for logging into profile, server side login button on Home page
    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.json  #get JSON data from request body
        username = data.get("username")
        password = data.get("password")

        result = verify_password(username, password) #call function to verify pw

        return jsonify(result) #return JSON response based on pw verification

    #GET method for personal profile (logged in user), server side view-profile
    @app.route("/api/view-profile", methods=["GET"])
    def view_profile_api():
        #return other user if queried, otherwise return logged in user
        user_id = request.headers.get("User-Id")
        data = get_profile(user_id)  #function to retrieve profile info from db

        if "error" in data:
            status_code = (
                404 if data["error"] == "User not found" else #id not found in db
                401 #unauthorized, user id missing
            )
            return jsonify(data), status_code

        return jsonify(data), 200  #return user profile data as JSON string, 200 success code
    
    #GET method for displaying other prfoiles
    @app.route("/api/view-recommendations", methods=["GET"])
    def view_recommendations_api():
        user_id = request.headers.get("User-Id")           #user's personal id

        last_seen_id = request.headers.get("Last-Seen-Id") #id of last seen profile

        data = get_next_profile(user_id, last_seen_id)  #function to retrieve next recomended profile

        if "error" in data:
            status_code = (
                404 if data["error"] == "User not found" else #id not found in db or no more profiles to view
                401 #unauthorized, user id missing
            )
            return jsonify(data), status_code

        return jsonify(data), 200  #return next recommended profile
    
    #PUT method for updating personal profile (logged in user), server side update-profile form
    @app.route("/api/update-profile", methods=["PUT"])
    def update_profile_api():
        user_id = request.headers.get("User-Id")
        data = request.json  #get JSON data from request body

        result = update_info(user_id, data)

        if "error" in data:
            status_code = (
                404 if data["error"] == "User not found" else #id not found in db
                400 if data["error"] == "No data to update" else #no data provided
                401 #unauthorized, user id missing
            )
            return jsonify(data), status_code
        
        return result, 200
    
    #POST method for liking a profile
    @app.route("/api/like-profile", methods=["POST"])
    def liked_profile_api():
        user_id = request.headers.get("User-Id")
        data = request.json  #get JSON data from request body
        liked_user_id = data.get("liked_user_id")

        result = add_liked_profile(user_id, liked_user_id)

        if "error" in result:
            status_code = (
                404 if result["error"] == "User not found" else #id not found in db
                400 if result["error"] == "Invalid User Id" else #invalid input
                401 #unauthorized, user id missing
            )
            return jsonify(result), status_code
        
        return jsonify(result), 200

    #GET method for viewing list of profiles who liked you
    @app.route("/api/view-likes", methods=["GET"])
    def view_likes_api():
        user_id = request.headers.get("User-Id")
        result = get_liked_profile(user_id)

        if "error" in result:
            status_code = (
                404 if result["error"] == "User not found" else
                401  # Unauthorized
            )
            return jsonify(result), status_code  # Ensures JSON response

        return jsonify(result), 200
    
    #api calls for updated liked and matched profile arrays
    #POST - skip button updates like_users array of logged in user
    @app.route("/api/skip-profile", methods=["POST"])
    def skip_profile_api():
        user_id = request.headers.get("User-Id")
        data = request.get_json()
        skipped_user_id = data.get("skipped_user_id")

        #Always add to skipped_users (if skipping from either view-likes or view-recommendations)
        add_result = add_skipped_profile(user_id, skipped_user_id)

        #If viewing from view-likes page, also remove the user from likes list. No action if viewing from view-recommendations.
        remove_result = remove_like(user_id, skipped_user_id)
        
        return jsonify({
            "skip_result": add_result,
            "like_removal_result": remove_result
        }), 200
    
    #POST - match button updates both user's matched_profile array with other user
    @app.route("/api/match-profile", methods=["POST"])
    def match_profile_api():
        user_id = request.headers.get("User-Id")
        data = request.get_json()
        liked_user_id = data.get("liked_user_id")

        result = add_match(user_id, liked_user_id)
        return jsonify(result), 200
    
    