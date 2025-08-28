# ==============================================================================
# File: backend/core/inference.py
# Description: Handles the actual machine learning model loading and prediction.
# THIS FILE NOW CONTAINS YOUR REAL-TIME DETECTION LOGIC.
# ==============================================================================
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import librosa
import noisereduce as nr
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LSTM

# --- Custom LSTM Class for Voice Model ---
# As required by your voice model loading script
class CustomLSTM(LSTM):
    def __init__(self, *args, **kwargs):
        kwargs.pop("time_major", None)
        super().__init__(*args, **kwargs)

# --- Global Variables for Models and Classifiers ---
# These will be loaded once when the server starts.
face_emotion_model = None
voice_emotion_model = None
face_cascade = None
FACE_EMOTION_LABELS = ['angry', 'neutral', 'sleep', 'stress']
VOICE_EMOTION_LABELS = ['sleepy', 'angry', 'stress'] # Note: 'sleepy' vs 'sleep'

# --- Model Loading Functions ---

def load_models(face_model_path, voice_model_path, cascade_path):
    """
    Loads all ML models and classifiers from their specified paths.
    This function is called once when the server starts.
    """
    global face_emotion_model, voice_emotion_model, face_cascade
    
    # Load Haar cascade for face detection
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            print(f"[Inference] Error: Haar cascade file not found or failed to load from {cascade_path}")
        else:
            print(f"[Inference] Haar cascade loaded successfully.")
    except Exception as e:
        print(f"[Inference] Error loading Haar cascade: {e}")

    # Load facial emotion model
    try:
        face_emotion_model = load_model(face_model_path)
        print(f"[Inference] Facial emotion model loaded successfully from {face_model_path}")
    except Exception as e:
        print(f"[Inference] Error loading facial emotion model: {e}")
        face_emotion_model = None

    # Load voice emotion model
    try:
        voice_emotion_model = load_model(voice_model_path, custom_objects={'LSTM': CustomLSTM})
        print(f"[Inference] Voice emotion model loaded successfully from {voice_model_path}")
    except Exception as e:
        print(f"[Inference] Error loading voice emotion model: {e}")
        voice_emotion_model = None


# --- Prediction Functions ---

def predict_emotion_from_image(base64_string):
    """
    Takes a base64 encoded image string, preprocesses it using your logic,
    and returns a predicted emotion string.
    """
    if face_emotion_model is None or face_cascade is None:
        return "Facial Model Not Ready"

    # 1. Decode Base64 string to an OpenCV image
    if "," in base64_string:
        base64_string = base64_string.split(',')[1]
    img_bytes = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 2. Preprocess the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # If no face is detected, return Neutral
    if len(faces) == 0:
        return "Neutral"

    # Assume only one face, the largest one
    (x, y, w, h) = faces[0]
    face_gray = gray[y:y+h, x:x+w]
    face_gray = cv2.resize(face_gray, (48, 48))

    # Apply CLAHE as in your script
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    face_gray = clahe.apply(face_gray)

    # Normalize and reshape for the model
    face_gray = face_gray.astype('float32') / 255.0
    face_gray = np.reshape(face_gray, (1, 48, 48, 1))

    # 3. Make prediction
    prediction = face_emotion_model.predict(face_gray)
    confidence = np.max(prediction)

    # Only return a prediction if confidence is above a threshold
    if confidence > 0.4:
        predicted_emotion = FACE_EMOTION_LABELS[np.argmax(prediction)]
        return predicted_emotion.capitalize()
    else:
        return "Neutral"

def predict_emotion_from_audio(base64_audio_string, sample_rate=22050):
    """
    Takes a base64 encoded audio string, preprocesses it, and returns a prediction.
    NOTE: This function is ready but not yet used by the API endpoint.
    """
    if voice_emotion_model is None:
        return "Voice Model Not Ready"

    # 1. Decode Base64 audio
    if "," in base64_audio_string:
        base64_audio_string = base64_audio_string.split(',')[1]
    audio_bytes = base64.b64decode(base64_audio_string)
    
    # Convert bytes to a numpy float array that librosa can use
    audio, _ = librosa.load(BytesIO(audio_bytes), sr=sample_rate)

    # 2. Extract features using your logic
    try:
        audio, _ = librosa.effects.trim(audio)
        audio = librosa.util.normalize(audio)
        audio = nr.reduce_noise(y=audio, sr=sample_rate)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        features = mfccs_mean.reshape(1, 1, 40)
    except Exception as e:
        print(f"Feature extraction error: {e}")
        return "Processing Error"

    # 3. Make prediction
    prediction = voice_emotion_model.predict(features)[0]
    emotion_index = np.argmax(prediction)
    predicted_emotion = VOICE_EMOTION_LABELS[emotion_index]
    
    return predicted_emotion.capitalize()


# --- Initial Model Loading ---
# This code runs when the server starts, loading the models into memory.
from config import Config
load_models(Config.FACE_MODEL_PATH, Config.VOICE_MODEL_PATH, Config.CASCADE_PATH)
