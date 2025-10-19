"""
Flask Application Factory for MoodMate Backend
"""

from flask import Flask
from flask_cors import CORS
from datetime import datetime
import json
import os

# Import the blueprint from routes file
from api.routes import main_bp

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
PET_DATA_FILE = os.path.join(DATA_DIR, 'pet_data.json')
MOOD_HISTORY_FILE = os.path.join(DATA_DIR, 'mood_history.json')

def save_json_file(filepath, data):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def init_default_data():
    """Initialize default data files if they don't exist"""
    # Create data directory
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Initialize users file
    if not os.path.exists(USERS_FILE):
        default_users = {
            "users": [
                {
                    "id": 1,
                    "username": "User",
                    "email": "user@example.com",
                    "bio": "Hello! I'm using MoodMate to track and understand my emotions better.",
                    "hobbies": "Reading, Music, Hiking, Photography",
                    "created_at": datetime.now().isoformat()
                }
            ]
        }
        save_json_file(USERS_FILE, default_users)
        print(f"✅ Created default users file: {USERS_FILE}")
    
    # Initialize pet data file
    if not os.path.exists(PET_DATA_FILE):
        default_pet = {
            "1": {
                "pet_name": "Buddy",
                "pet_mood": "happy",
                "pet_level": 1,
                "pet_exp": 0,
                "happiness": 80,
                "energy": 65,
                "hunger": 30,
                "last_fed": datetime.now().isoformat()
            }
        }
        save_json_file(PET_DATA_FILE, default_pet)
        print(f"✅ Created default pet data file: {PET_DATA_FILE}")
    
    # Initialize mood history file
    if not os.path.exists(MOOD_HISTORY_FILE):
        save_json_file(MOOD_HISTORY_FILE, [])
        print(f"✅ Created mood history file: {MOOD_HISTORY_FILE}")

def create_app():
    """Creates and configures the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    from config import Config
    app.config.from_object(Config)
    
    # Enable CORS for frontend integration
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Register the API blueprint
    # All routes in api_bp will be prefixed with /api
    app.register_blueprint(main_bp, url_prefix='/api')

    print("✅ Flask App Created")
    print("✅ CORS Enabled")
    print("✅ API Blueprint Registered with prefix '/api'")
    
    return app