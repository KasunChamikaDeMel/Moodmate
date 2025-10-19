import os
import json
import time
try:
    import importlib
    _dotenv = importlib.import_module('dotenv')
    load_dotenv = getattr(_dotenv, 'load_dotenv')
except Exception:
    # If python-dotenv is not available, provide a no-op fallback to avoid import errors
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kasun'
    
    # Database configuration
    # SQLite (for development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'moodmate.db')
    
    # For MySQL (uncomment and configure if needed)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'mysql+pymysql://username:password@localhost/moodmate'
    
    # For PostgreSQL (uncomment and configure if needed)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'postgresql://username:password@localhost/moodmate'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Data and models directories
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    
    # Model paths
    FACE_MODEL_PATH = os.path.join(MODELS_DIR, 'facial_emotion_model.h5')
    VOICE_MODEL_PATH = os.path.join(MODELS_DIR, 'voice_emotion_model.h5')
    
    # OpenCV Haar Cascade path
    CASCADE_PATH = os.path.join(MODELS_DIR, 'haarcascade_frontalface_default.xml')
    
    # Other directories
    AUDIO_DIR = os.path.join(DATA_DIR, 'audio')
    IMAGES_DIR = os.path.join(DATA_DIR, 'images')
    UPLOADS_DIR = os.path.join(DATA_DIR, 'uploads')
    
    # Data files - ADD THESE LINES
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    PET_DATA_FILE = os.path.join(DATA_DIR, 'pets.json')
    EMOTION_HISTORY_FILE = os.path.join(DATA_DIR, 'emotion_history.json')
    MOOD_HISTORY_FILE = os.path.join(DATA_DIR, 'mood_history.json')
    USER_SETTINGS_FILE = os.path.join(DATA_DIR, 'user_settings.json')
    SESSION_DATA_FILE = os.path.join(DATA_DIR, 'session_data.json')
    ANALYTICS_FILE = os.path.join(DATA_DIR, 'analytics.json')

    # Utility functions (keep these for now, we'll migrate to SQL)
    @staticmethod
    def save_json_file(file_path, data):
        """Save data to a JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
            return False

    @staticmethod
    def load_json_file(file_path):
        """Load data from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}

    @classmethod
    def ensure_directories_exist(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_DIR,
            cls.MODELS_DIR,
            cls.AUDIO_DIR,
            cls.IMAGES_DIR,
            cls.UPLOADS_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @classmethod
    def ensure_data_files(cls):
        """Create data directory and files if they don't exist"""
        cls.ensure_directories_exist()
        
        # Create empty JSON files if they don't exist
        files_to_create = [
            cls.USERS_FILE, 
            cls.PET_DATA_FILE, 
            cls.EMOTION_HISTORY_FILE,
            cls.MOOD_HISTORY_FILE,
            cls.USER_SETTINGS_FILE,
            cls.SESSION_DATA_FILE,
            cls.ANALYTICS_FILE
        ]
        
        for file_path in files_to_create:
            if not os.path.exists(file_path):
                cls.save_json_file(file_path, {})
                print(f"✅ Created data file: {file_path}")
        
        # Initialize default data
        cls.initialize_default_data()

    @classmethod
    def initialize_default_data(cls):
        """Create default user and pet if they don't exist"""
        users = cls.load_json_file(cls.USERS_FILE)
        if not users:
            users['1'] = {
                "id": "1",
                "name": "Default User",
                "email": "user@example.com",
                "created_at": time.time()
            }
            cls.save_json_file(cls.USERS_FILE, users)
            print("✅ Created default user")
        
        pets = cls.load_json_file(cls.PET_DATA_FILE)
        if not pets:
            pets['1'] = {
                "id": "1",
                "name": "Moody",
                "type": "virtual_pet",
                "mood": "happy",
                "level": 1,
                "created_at": time.time()
            }
            cls.save_json_file(cls.PET_DATA_FILE, pets)
            print("✅ Created default pet")