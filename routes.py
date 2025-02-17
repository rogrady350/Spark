from flask import render_template, request, jsonify
from service import add_profile

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
    
    @app.route("/create-profile")
    def create_profile():
        return render_template("create-profile.html")
    
    #API routes for crud operations (handle front end ajax requests)
    #POST method for submitting data to db, create-profile form
    @app.route("/api/create-profile", methods=["POST"])
    def create_profile_api():
        data=request.get_json() #get JSON string from request body
        result = add_profile(data) #insert into MongoDB
        
        if "Error" in result["msg"]:
            return jsonify(result), 400  #HTTP 400 (Bad Request) for errors
        
        return jsonify(result), 201 #HTTP 201 (Created) for successful profile creations
    
    #POST method for login
    