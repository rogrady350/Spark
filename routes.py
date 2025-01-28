from flask import render_template

#routes to pages
def init_routes(app):
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