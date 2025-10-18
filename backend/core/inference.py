import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import librosa
import noisereduce as nr
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LSTM
from textblob import TextBlob

class CustomLSTM(LSTM):
    def __init__(self, *args, **kwargs):
        kwargs.pop("time_major", None)
        super().__init__(*args, **kwargs)
face_emotion_model = None
voice_emotion_model = None
face_cascade = None
FACE_EMOTION_LABELS = ['angry', 'neutral', 'sleep', 'stress']
VOICE_EMOTION_LABELS = ['sleepy', 'angry', 'stress']

def load_models(face_model_path, voice_model_path, cascade_path):
    global face_emotion_model, voice_emotion_model, face_cascade
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
        print(f"[Inference] Haar cascade loaded.")
    except Exception as e:
        print(f"[Inference] Error loading Haar cascade: {e}")
    try:
        face_emotion_model = load_model(face_model_path)
        print(f"[Inference] Facial emotion model loaded.")
    except Exception as e:
        print(f"[Inference] Error loading facial model: {e}")
    try:
        voice_emotion_model = load_model(voice_model_path, custom_objects={'LSTM': CustomLSTM})
        print(f"[Inference] Voice emotion model loaded.")
    except Exception as e:
        print(f"[Inference] Error loading voice model: {e}")

def predict_emotion_from_image(base64_string):
    if face_emotion_model is None or face_cascade is None: return "Facial Model Not Ready"
    if "," in base64_string: base64_string = base64_string.split(',')[1]
    img_bytes = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    if len(faces) == 0: return "Neutral"
    (x, y, w, h) = faces[0]
    face_gray = gray[y:y+h, x:x+w]
    face_gray = cv2.resize(face_gray, (48, 48))
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    face_gray = clahe.apply(face_gray)
    face_gray = face_gray.astype('float32') / 255.0
    face_gray = np.reshape(face_gray, (1, 48, 48, 1))
    prediction = face_emotion_model.predict(face_gray)
    if np.max(prediction) > 0.4:
        return FACE_EMOTION_LABELS[np.argmax(prediction)].capitalize()
    return "Neutral"

def predict_emotion_from_audio(base64_audio_string, sample_rate=22050):
    if voice_emotion_model is None: return "Voice Model Not Ready"
    if "," in base64_audio_string: base64_audio_string = base64_audio_string.split(',')[1]
    audio_bytes = base64.b64decode(base64_audio_string)
    audio, _ = librosa.load(BytesIO(audio_bytes), sr=sample_rate)
    try:
        audio, _ = librosa.effects.trim(audio)
        audio = librosa.util.normalize(audio)
        audio = nr.reduce_noise(y=audio, sr=sample_rate)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        features = np.mean(mfccs.T, axis=0).reshape(1, 1, 40)
    except Exception as e:
        return "Processing Error"
    prediction = voice_emotion_model.predict(features)[0]
    return VOICE_EMOTION_LABELS[np.argmax(prediction)].capitalize()

def predict_emotion_from_text(text):
    """
    Analyzes text sentiment to infer emotion.
    This is a placeholder and can be replaced with a more advanced NLP model.
    """
    if not text.strip():
        return "Neutral"
        
    analysis = TextBlob(text)
    # Polarity is between -1 (negative) and 1 (positive)
    if analysis.sentiment.polarity < -0.3:
        return "Angry"
    elif analysis.sentiment.polarity > 0.3:
        return "Happy" # Assuming happy is a positive neutral state for this context
    else:
        # Subjectivity is between 0 (objective) and 1 (subjective)
        if analysis.sentiment.subjectivity > 0.6:
            return "Stress" # High subjectivity can indicate stress
        else:
            return "Neutral"

from config import Config
load_models(Config.FACE_MODEL_PATH, Config.VOICE_MODEL_PATH, Config.CASCADE_PATH)
