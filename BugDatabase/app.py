from flask import Flask
from flask_cors import CORS
from endpoints import bugCRUD   # Import endpoints
from gateway import utility     # Import gateway startup
import os

# Create the flask application and make it CORS compliant
app = Flask(__name__)
CORS(app)

# Change the configuration settings of the app
app.config.from_object("resources.config.Config")   # Import app config file

# Runs this code once the app starts but before the first request
@app.before_first_request
def before_first_request():
    # Create database and table if they don't exist
    utility.check_database()
    utility.check_tables()


# Add endpoints
app.add_url_rule('/bugs', view_func=bugCRUD.get_bugs, methods=['GET'])
app.add_url_rule('/bugs', view_func=bugCRUD.create_bug, methods=['POST'])
#app.add_url_rule('/bugs/<id>', view_func=bugCRUD.get_one_bug, methods=['GET'])
app.add_url_rule('/bugs/<id>', view_func=bugCRUD.update_bug, methods=['PUT'])
app.add_url_rule('/bugs/<id>', view_func=bugCRUD.delete_bug, methods=['DELETE'])

# Run it
if __name__ == '__main__':
    app.run()