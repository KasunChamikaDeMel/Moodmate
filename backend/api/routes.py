

from flask import Blueprint, request, jsonify
from core.inference import predict_emotion_from_image, predict_emotion_from_audio, predict_emotion_from_text
import time
import os
import json
from datetime import datetime
from config import Config

# Create the blueprint
main_bp = Blueprint('main', __name__)

# Data file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_FILE = Config.USERS_FILE
PET_DATA_FILE = Config.PET_DATA_FILE
MOOD_HISTORY_FILE = Config.MOOD_HISTORY_FILE

# Utility functions
def save_json_file(file_path, data):
    """Save data to a JSON file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def load_json_file(file_path):
    """Load data from a JSON file"""
    try:
        if not os.path.exists(file_path):
            return [] if 'history' in file_path else {}
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return [] if 'history' in file_path else {}

def init_data_files():
    """Initialize data files with default data"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Initialize users file
    if not os.path.exists(USERS_FILE):
        default_users = {
            "users": [{
                "id": 1,
                "username": "User",
                "email": "user@example.com",
                "bio": "Hello! I'm using MoodMate.",
                "created_at": datetime.now().isoformat()
            }]
        }
        save_json_file(USERS_FILE, default_users)
        print(f"✅ Created users file")
    
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
        print(f"✅ Created pet data file")
    
    # Initialize mood history (as list)
    if not os.path.exists(MOOD_HISTORY_FILE):
        save_json_file(MOOD_HISTORY_FILE, [])
        print(f"✅ Created mood history file")

# Initialize on import
init_data_files()

# ============= ROUTES =============

@main_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "models_loaded": True,
        "timestamp": time.time()
    })

@main_bp.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({
        "message": "MoodMate API is working!", 
        "status": "success",
        "models_loaded": True
    })

# ============= EMOTION DETECTION =============

@main_bp.route('/predict_face', methods=['POST'])
def predict_face():
    """Face emotion prediction"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "Missing 'image' data"}), 400
        
        emotion = predict_emotion_from_image(data['image'])
        
        # Add to mood history
        add_to_history(1, emotion, "face")
        
        return jsonify({
            "emotion": emotion,
            "timestamp": time.time(),
            "source": "face"
        })
    except Exception as e:
        print(f"Face prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/predict_voice', methods=['POST'])
def predict_voice():
    """Voice emotion prediction"""
    try:
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({"error": "Missing 'audio' data"}), 400

        emotion = predict_emotion_from_audio(data['audio'])
        
        # Add to mood history
        add_to_history(1, emotion, "voice")
        
        return jsonify({
            "emotion": emotion,
            "timestamp": time.time(),
            "source": "voice"
        })
    except Exception as e:
        print(f"Voice prediction error: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/predict_text', methods=['POST'])
def predict_text():
    """Text emotion prediction"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' data"}), 400

        emotion = predict_emotion_from_text(data['text'])
        
        # Add to mood history
        add_to_history(1, emotion, "text")
        
        return jsonify({
            "emotion": emotion,
            "timestamp": time.time(),
            "source": "text"
        })
    except Exception as e:
        print(f"Text prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# ============= MOOD HISTORY =============

def add_to_history(user_id, mood, source):
    """Helper function to add mood to history"""
    try:
        history = load_json_file(MOOD_HISTORY_FILE)
        
        entry = {
            "user_id": str(user_id),
            "mood": mood.lower(),
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        
        history.append(entry)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        save_json_file(MOOD_HISTORY_FILE, history)
        return True
    except Exception as e:
        print(f"Error adding to history: {e}")
        return False

@main_bp.route('/mood_history/<user_id>', methods=['GET'])
def get_user_mood_history(user_id):
    """Get mood history for specific user"""
    try:
        history = load_json_file(MOOD_HISTORY_FILE)
        
        # Filter by user_id
        user_history = [
            entry for entry in history 
            if str(entry.get('user_id', '1')) == str(user_id)
        ]
        
        # Sort by timestamp (newest first)
        user_history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify(user_history)
    except Exception as e:
        print(f"Error getting mood history: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/mood_history', methods=['POST'])
def add_mood_history():
    """Add mood history entry"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', '1')
        mood = data.get('mood', 'neutral')
        source = data.get('source', 'manual')
        
        success = add_to_history(user_id, mood, source)
        
        if success:
            return jsonify({
                "message": "Mood added to history",
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": "Failed to add mood"}), 500
    except Exception as e:
        print(f"Error adding mood: {e}")
        return jsonify({"error": str(e)}), 500

# ============= USER MANAGEMENT =============

@main_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user information"""
    try:
        users_data = load_json_file(USERS_FILE)
        users = users_data.get('users', [])
        
        user = next((u for u in users if u.get('id') == user_id), None)
        
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    try:
        data = request.get_json()
        users_data = load_json_file(USERS_FILE)
        users = users_data.get('users', [])
        
        for i, user in enumerate(users):
            if user.get('id') == user_id:
                users[i].update(data)
                users[i]['updated_at'] = datetime.now().isoformat()
                users_data['users'] = users
                save_json_file(USERS_FILE, users_data)
                return jsonify(users[i])
        
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": str(e)}), 500

# ============= PET MANAGEMENT =============

@main_bp.route('/pet/<int:user_id>', methods=['GET'])
def get_pet_data(user_id):
    """Get pet data for user"""
    try:
        pets = load_json_file(PET_DATA_FILE)
        pet = pets.get(str(user_id))
        
        if pet:
            return jsonify(pet)
        else:
            # Return default pet
            default_pet = {
                "pet_name": "Buddy",
                "pet_mood": "happy",
                "pet_level": 1,
                "pet_exp": 0,
                "happiness": 80,
                "energy": 65,
                "hunger": 30
            }
            return jsonify(default_pet)
    except Exception as e:
        print(f"Error getting pet: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/pet/<int:user_id>', methods=['PUT'])
def update_pet_data(user_id):
    """Update pet data"""
    try:
        data = request.get_json()
        pets = load_json_file(PET_DATA_FILE)
        
        pet_key = str(user_id)
        if pet_key not in pets:
            pets[pet_key] = {}
        
        pets[pet_key].update(data)
        pets[pet_key]['last_updated'] = datetime.now().isoformat()
        
        save_json_file(PET_DATA_FILE, pets)
        return jsonify(pets[pet_key])
    except Exception as e:
        print(f"Error updating pet: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/pet/<int:user_id>/feed', methods=['POST'])
def feed_pet(user_id):
    """Feed the pet"""
    try:
        pets = load_json_file(PET_DATA_FILE)
        pet_key = str(user_id)
        
        if pet_key not in pets:
            return jsonify({"error": "Pet not found"}), 404
        
        # Update pet stats
        pet = pets[pet_key]
        pet['hunger'] = max(0, pet.get('hunger', 30) - 20)
        pet['happiness'] = min(100, pet.get('happiness', 80) + 10)
        pet['pet_exp'] = min(100, pet.get('pet_exp', 0) + 5)
        pet['last_fed'] = datetime.now().isoformat()
        pet['pet_mood'] = 'happy'
        
        save_json_file(PET_DATA_FILE, pets)
        return jsonify(pet)
    except Exception as e:
        print(f"Error feeding pet: {e}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/pet/<int:user_id>/mood', methods=['PUT'])
def update_pet_mood(user_id):
    """Update pet mood"""
    try:
        data = request.get_json()
        mood = data.get('mood', 'happy')
        
        pets = load_json_file(PET_DATA_FILE)
        pet_key = str(user_id)
        
        if pet_key not in pets:
            pets[pet_key] = {
                "pet_name": "Buddy",
                "pet_level": 1,
                "pet_exp": 0
            }
        
        pets[pet_key]['pet_mood'] = mood
        pets[pet_key]['last_updated'] = datetime.now().isoformat()
        
        save_json_file(PET_DATA_FILE, pets)
        return jsonify(pets[pet_key])
    except Exception as e:
        print(f"Error updating pet mood: {e}")
        return jsonify({"error": str(e)}), 500

print("✅ Backend routes loaded successfully")