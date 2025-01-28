from flask import Flask
from routes import init_routes #set up page listeners

app = Flask(__name__)

#initialize 
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)