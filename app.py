from flask import Flask
from routes import init_routes #set up page listeners

#Flask app setup - define app instance
app = Flask(__name__)

#initialize routes
init_routes(app)

#run app in development mode
if __name__ == "__main__":
    app.run(debug=True) #start app