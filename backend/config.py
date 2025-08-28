# ==============================================================================
# File: backend/config.py
# Description: Centralized configuration for the Flask application.
# ==============================================================================
import os
import cv2

class Config:
    """Base configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'

    # Server settings
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True

    # --- Path to ML models and classifiers ---
    # Get the directory of the current file
    BASE_DIR = os.path.dirname(__file__)

    FACE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'facial_emotion_model.h5')
    VOICE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'voice_emotion_detector.h5')
    
    # Path to the Haar cascade file provided by OpenCV
    CASCADE_PATH = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
