from flask import render_template, request, jsonify
from service import add_profile, verify_password, get_profile

def init_routes(app):
    #routes to pages
    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/view-profile")
    def view_profile():
        return render_template("view-profile.html")

    @app.route("/view-recommendations")
    def view_recommendations():
        return render_template("view-recommendations.html")
    
    @app.route("/update-profile")
    def update_profile():
        return render_template("update-profile.html")
    
    @app.route("/create-account")
    def create_account():
        return render_template("create-account.html")
    
    #API routes for crud operations (handle front end ajax requests)
    #POST method for submitting data to db, server side create-account form
    @app.route("/api/create-account", methods=["POST"])
    def create_account_api():
        data = request.json() #get JSON string from request body
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

    #GET method for personal profile (logged in user)
    @app.route("/api/view-profile", methods=["GET"])
    def view_profile_api():
        #return other user if queried, otherwise return logged in user
        user_id = request.headers.get("User-Id")

        profile_data = get_profile(user_id)  #function to retrieve profile info from db

        if "error" in profile_data:
            #401: unauthorized, user id missing. 404: id not found in db
            status_code = 401 if profile_data["error"] == "Unauthorized" else 404
            return jsonify(profile_data), status_code

        return jsonify(profile_data)  #Return user profile data as JSON string
