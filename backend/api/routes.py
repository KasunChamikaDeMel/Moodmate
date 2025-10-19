from flask import Blueprint, request, jsonify
from core.inference import predict_emotion_from_image, predict_emotion_from_audio, predict_emotion_from_text
import time
import os
import json
from config import Config

# Add ALL data file configuration variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Define all possible data files
USERS_FILE = Config.USERS_FILE
PET_DATA_FILE = Config.PET_DATA_FILE
EMOTION_HISTORY_FILE = Config.EMOTION_HISTORY_FILE
MOOD_HISTORY_FILE = Config.MOOD_HISTORY_FILE
USER_SETTINGS_FILE = Config.USER_SETTINGS_FILE
SESSION_DATA_FILE = Config.SESSION_DATA_FILE
ANALYTICS_FILE = Config.ANALYTICS_FILE

# Use Config's utility functions
save_json_file = Config.save_json_file
load_json_file = Config.load_json_file

# Create the blueprint
main_bp = Blueprint('main', __name__)

# Initialize data files using Config
Config.ensure_data_files()

# Utility functions
def save_json_file(file_path, data):
    """Save data to a JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def load_json_file(file_path):
    """Load data from a JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def ensure_data_files():
    """Create data directory and files if they don't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create empty JSON files if they don't exist
    files_to_create = [
        USERS_FILE, 
        PET_DATA_FILE, 
        EMOTION_HISTORY_FILE,
        MOOD_HISTORY_FILE,
        USER_SETTINGS_FILE,
        SESSION_DATA_FILE,
        ANALYTICS_FILE
    ]
    
    for file_path in files_to_create:
        if not os.path.exists(file_path):
            save_json_file(file_path, {})
            print(f"✅ Created data file: {file_path}")

# Initialize data files
ensure_data_files()

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "MoodMate Backend API",
        "status": "running", 
        "endpoints": {
            "health": "/api/health",
            "test": "/api/test",
            "users": "/api/users",
            "mood_history": "/api/mood_history",
            "predict_face": "/api/predict_face",
            "predict_voice": "/api/predict_voice", 
            "predict_text": "/api/predict_text"
        }
    })

# Test route
@main_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        "message": "MoodMate API is working!", 
        "status": "success",
        "models_loaded": True,
        "data_files_ready": True
    })

# Face emotion prediction
@main_bp.route('/predict_face', methods=['POST'])
def predict_face():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "Missing 'image' data"}), 400
        
        from core.inference import predict_emotion_from_image
        emotion = predict_emotion_from_image(data['image'])
        return jsonify({"emotion": emotion, "timestamp": time.time()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Voice emotion prediction
@main_bp.route('/predict_voice', methods=['POST'])
def predict_voice():
    try:
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({"error": "Missing 'audio' data"}), 400

        from core.inference import predict_emotion_from_audio
        emotion = predict_emotion_from_audio(data['audio'])
        return jsonify({"emotion": emotion, "timestamp": time.time()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Text emotion prediction
@main_bp.route('/predict_text', methods=['POST'])
def predict_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' data"}), 400

        from core.inference import predict_emotion_from_text
        emotion = predict_emotion_from_text(data['text'])
        return jsonify({"emotion": emotion, "timestamp": time.time()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Mood history routes
@main_bp.route('/mood_history', methods=['GET'])
def get_mood_history():
    try:
        history = load_json_file(MOOD_HISTORY_FILE)
        return jsonify({"mood_history": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Get mood history for a specific user
@main_bp.route('/mood_history/<user_id>', methods=['GET'])
def get_user_mood_history(user_id):
    try:
        history = load_json_file(MOOD_HISTORY_FILE)
        
        # Handle both list and dictionary formats
        user_history = {}
        
        if isinstance(history, dict):
            # Dictionary format: {timestamp: entry}
            for timestamp, entry in history.items():
                entry_user_id = entry.get('user_id', '1')
                if entry_user_id == user_id:
                    user_history[timestamp] = entry
        elif isinstance(history, list):
            # List format: [entry1, entry2, ...]
            for i, entry in enumerate(history):
                entry_user_id = entry.get('user_id', '1')
                if entry_user_id == user_id:
                    # Use index as key or generate timestamp key
                    timestamp = entry.get('timestamp', f"entry_{i}")
                    user_history[timestamp] = entry
        
        return jsonify({
            "user_id": user_id, 
            "mood_history": user_history,
            "total_entries": len(user_history)
        })
    except Exception as e:
        print(f"❌ Error in get_user_mood_history: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

@main_bp.route('/mood_history', methods=['POST'])
def add_mood_history():
    try:
        data = request.get_json()
        history = load_json_file(MOOD_HISTORY_FILE)
        
        # Ensure history is a dictionary
        if isinstance(history, list):
            # Convert list to dictionary
            new_history = {}
            for i, entry in enumerate(history):
                timestamp = entry.get('timestamp', f"entry_{i}")
                new_history[timestamp] = entry
            history = new_history
            save_json_file(MOOD_HISTORY_FILE, history)
        
        # Add new mood entry
        timestamp = str(time.time())
        
        # Ensure user_id is included
        if 'user_id' not in data:
            data['user_id'] = '1'
            
        history[timestamp] = data
        
        save_json_file(MOOD_HISTORY_FILE, history)
        return jsonify({"message": "Mood added to history", "timestamp": timestamp})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User management routes
@main_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = load_json_file(USERS_FILE)
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        users = load_json_file(USERS_FILE)
        
        user_id = data.get('id', str(time.time()))
        users[user_id] = data
        
        save_json_file(USERS_FILE, users)
        return jsonify({"message": "User added", "user_id": user_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "models_loaded": True,
        "timestamp": time.time()
    })

# Add these missing routes that the frontend is trying to access:

# User routes
@main_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        users = load_json_file(USERS_FILE)
        user = users.get(user_id)
        if user:
            return jsonify({"user": user})
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Pet routes
@main_bp.route('/pets', methods=['GET'])
def get_pets():
    try:
        pets = load_json_file(PET_DATA_FILE)
        return jsonify({"pets": pets})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/pet/<pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        pets = load_json_file(PET_DATA_FILE)
        pet = pets.get(pet_id)
        if pet:
            return jsonify({"pet": pet})
        else:
            return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/pet/<pet_id>/mood', methods=['PUT'])
def update_pet_mood(pet_id):
    try:
        data = request.get_json()
        pets = load_json_file(PET_DATA_FILE)
        
        if pet_id not in pets:
            # Create a default pet if it doesn't exist
            pets[pet_id] = {
                "id": pet_id,
                "name": "Moody",
                "type": "virtual_pet", 
                "mood": "happy",
                "level": 1,
                "created_at": time.time()
            }
        
        # Update the pet's mood
        pets[pet_id]['mood'] = data.get('mood', 'happy')
        pets[pet_id]['last_updated'] = time.time()
        
        save_json_file(PET_DATA_FILE, pets)
        return jsonify({
            "message": "Pet mood updated", 
            "pet_id": pet_id,
            "mood": pets[pet_id]['mood']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create default data if files are empty
def initialize_default_data():
    """Create default user and pet if they don't exist"""
    users = load_json_file(USERS_FILE)
    if not users:
        users['1'] = {
            "id": "1",
            "name": "Default User",
            "email": "user@example.com",
            "created_at": time.time()
        }
        save_json_file(USERS_FILE, users)
        print("✅ Created default user")
    
    pets = load_json_file(PET_DATA_FILE)
    if not pets:
        pets['1'] = {
            "id": "1",
            "name": "Moody",
            "type": "virtual_pet",
            "mood": "happy",
            "level": 1,
            "created_at": time.time()
        }
        save_json_file(PET_DATA_FILE, pets)
        print("✅ Created default pet")

# Initialize default data
initialize_default_data()