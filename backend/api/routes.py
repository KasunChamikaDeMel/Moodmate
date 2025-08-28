from flask import Blueprint, request, jsonify
from core.inference import predict_emotion_from_image, predict_emotion_from_audio, predict_emotion_from_text
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/predict_face', methods=['POST'])
def predict_face():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Missing 'image' data"}), 400
    
    emotion = predict_emotion_from_image(data['image'])
    return jsonify({"emotion": emotion, "timestamp": time.time()})

@main_bp.route('/predict_voice', methods=['POST'])
def predict_voice():
    data = request.get_json()
    if not data or 'audio' not in data:
        return jsonify({"error": "Missing 'audio' data"}), 400

    emotion = predict_emotion_from_audio(data['audio'])
    return jsonify({"emotion": emotion, "timestamp": time.time()})

@main_bp.route('/predict_text', methods=['POST'])
def predict_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' data"}), 400

    emotion = predict_emotion_from_text(data['text'])
    return jsonify({"emotion": emotion, "timestamp": time.time()})