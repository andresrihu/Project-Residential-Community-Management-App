from flask_app import app
from flask_app.controllers import resident_controller, project_controller, message_controller

if __name__ == "__main__":
    app.run(debug=True)