from flask import Flask
from flask_cors import CORS
from app.routes import api_bp  # ✅ Ensure this file exists

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

app.register_blueprint(api_bp, url_prefix="/api")  # ✅ Register the Blueprint
