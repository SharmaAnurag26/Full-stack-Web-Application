from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from routes import all_blueprints  # This assumes routes is in the same folder as app.py

    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app
