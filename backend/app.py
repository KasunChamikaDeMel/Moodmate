from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Data storage (in production, use a proper database)
USERS_FILE = 'data/users.json'
MOOD_HISTORY_FILE = 'data/mood_history.json'
PET_DATA_FILE = 'data/pet_data.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def load_json_file(filename, default_data):
    """Load data from JSON file or return default if file doesn't exist"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return default_data
    except:
        return default_data

def save_json_file(filename, data):
    """Save data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except:
        return False

# Initialize default data
def init_default_data():
    """Initialize default data files if they don't exist"""
    if not os.path.exists(USERS_FILE):
        default_users = {
            "users": [
                {
                    "id": 1,
                    "username": "User",
                    "email": "user@example.com",
                    "created_at": datetime.now().isoformat()
                }
            ]
        }
        save_json_file(USERS_FILE, default_users)
    
    if not os.path.exists(PET_DATA_FILE):
        default_pet = {
            "pet_name": "Buddy",
            "pet_mood": "happy",
            "pet_level": 1,
            "pet_exp": 0,
            "last_fed": datetime.now().isoformat()
        }
        save_json_file(PET_DATA_FILE, default_pet)
    
    if not os.path.exists(MOOD_HISTORY_FILE):
        default_history = []
        save_json_file(MOOD_HISTORY_FILE, default_history)

# Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "MoodMate Backend is running"})

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Get user profile information"""
    users = load_json_file(USERS_FILE, {"users": []})
    if users["users"]:
        return jsonify(users["users"][0])
    return jsonify({"error": "No user found"}), 404

@app.route('/api/user/profile', methods=['PUT'])
def update_user_profile():
    """Update user profile"""
    data = request.get_json()
    users = load_json_file(USERS_FILE, {"users": []})
    
    if users["users"]:
        users["users"][0].update(data)
        users["users"][0]["updated_at"] = datetime.now().isoformat()
        if save_json_file(USERS_FILE, users):
            return jsonify(users["users"][0])
        return jsonify({"error": "Failed to save profile"}), 500
    
    return jsonify({"error": "No user found"}), 404

@app.route('/api/pet/info', methods=['GET'])
def get_pet_info():
    """Get pet information"""
    pet_data = load_json_file(PET_DATA_FILE, {})
    return jsonify(pet_data)

@app.route('/api/pet/feed', methods=['POST'])
def feed_pet():
    """Feed the pet and update its mood"""
    pet_data = load_json_file(PET_DATA_FILE, {})
    
    # Update pet mood and experience
    pet_data["pet_mood"] = "happy"
    pet_data["pet_exp"] += 10
    pet_data["last_fed"] = datetime.now().isoformat()
    
    # Level up if enough experience
    if pet_data["pet_exp"] >= 100:
        pet_data["pet_level"] += 1
        pet_data["pet_exp"] = 0
    
    if save_json_file(PET_DATA_FILE, pet_data):
        return jsonify(pet_data)
    return jsonify({"error": "Failed to save pet data"}), 500

@app.route('/api/pet/play', methods=['POST'])
def play_with_pet():
    """Play with the pet and update its mood"""
    pet_data = load_json_file(PET_DATA_FILE, {})
    
    # Update pet mood and experience
    pet_data["pet_mood"] = "excited"
    pet_data["pet_exp"] += 15
    pet_data["last_played"] = datetime.now().isoformat()
    
    if save_json_file(PET_DATA_FILE, pet_data):
        return jsonify(pet_data)
    return jsonify({"error": "Failed to save pet data"}), 500

@app.route('/api/mood/current', methods=['GET'])
def get_current_mood():
    """Get current user mood"""
    history = load_json_file(MOOD_HISTORY_FILE, [])
    if history:
        return jsonify({"current_mood": history[-1]["mood"]})
    return jsonify({"current_mood": "neutral"})

@app.route('/api/mood/detect', methods=['POST'])
def detect_mood():
    """Process mood detection (placeholder for ML integration)"""
    data = request.get_json()
    
    # This is a placeholder - in real app, you'd integrate with ML model
    detected_mood = data.get('detected_mood', 'neutral')
    confidence = data.get('confidence', 0.8)
    
    # Save mood to history
    mood_entry = {
        "id": len(load_json_file(MOOD_HISTORY_FILE, [])) + 1,
        "mood": detected_mood,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat(),
        "notes": data.get('notes', '')
    }
    
    history = load_json_file(MOOD_HISTORY_FILE, [])
    history.append(mood_entry)
    
    if save_json_file(MOOD_HISTORY_FILE, history):
        return jsonify({
            "success": True,
            "detected_mood": detected_mood,
            "confidence": confidence,
            "mood_entry": mood_entry
        })
    
    return jsonify({"error": "Failed to save mood"}), 500

@app.route('/api/mood/history', methods=['GET'])
def get_mood_history():
    """Get mood history"""
    history = load_json_file(MOOD_HISTORY_FILE, [])
    return jsonify({"mood_history": history})

@app.route('/api/mood/history', methods=['POST'])
def add_mood_entry():
    """Add manual mood entry"""
    data = request.get_json()
    
    mood_entry = {
        "id": len(load_json_file(MOOD_HISTORY_FILE, [])) + 1,
        "mood": data.get('mood', 'neutral'),
        "confidence": 1.0,  # Manual entry has full confidence
        "timestamp": datetime.now().isoformat(),
        "notes": data.get('notes', '')
    }
    
    history = load_json_file(MOOD_HISTORY_FILE, [])
    history.append(mood_entry)
    
    if save_json_file(MOOD_HISTORY_FILE, history):
        return jsonify(mood_entry)
    
    return jsonify({"error": "Failed to save mood entry"}), 500

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get application settings"""
    settings = {
        "notifications_enabled": True,
        "auto_save": True,
        "theme": "light",
        "language": "en"
    }
    return jsonify(settings)

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """Update application settings"""
    data = request.get_json()
    # In a real app, you'd save these to a settings file
    return jsonify({"success": True, "settings": data})

if __name__ == '__main__':
    init_default_data()
    print("Starting MoodMate Backend...")
    print("Backend will be available at: http://localhost:5000")
    print("API Documentation available at: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
