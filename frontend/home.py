import sys
from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                              QLineEdit, QSizePolicy, QSpacerItem, QMessageBox, QProgressBar,
                              QGraphicsDropShadowEffect, QWidget)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QIcon, QFont, QColor
import cv2
import base64
import pyaudio
import wave
import io
from datetime import datetime, timedelta
from collections import Counter
import threading
from collections import deque
import time

# --- Use the REAL APIClient ---
from api_client import APIClient

# --- YOUR REAL EMOTION_FUSION.PY CODE ---
# (Included here as it was in your file)

class EmotionFusion:
    """Intelligent emotion fusion from multiple modalities"""
    
    WEIGHTS = {
        'face': 0.45,
        'voice': 0.40,
        'text': 0.15
    }
    
    def __init__(self, temporal_window=5):
        self.temporal_window = temporal_window
        self.recent_emotions = {
            'face': deque(maxlen=temporal_window),
            'voice': deque(maxlen=temporal_window),
            'text': deque(maxlen=temporal_window)
        }
        self.last_fused_emotion = "neutral"
        self.emotion_scores = {}
        self.lock = threading.Lock()
    
    # --- !!! LOGIC FIX 1: Normalize to ONLY your 4 emotions !!! ---
    def normalize_emotion(self, emotion):
        """
        Normalize emotion name variations to ONLY the 4 target emotions:
        Neutral, Stress, Sleep, Anger
        """
        emotion = emotion.lower().strip()
        
        # 1. Direct mappings for your target emotions
        if emotion in ['stress', 'stressed', 'fear']:
            return 'stress'
        if emotion in ['angry', 'anger']:
            return 'angry'
        if emotion in ['sleep', 'sleepy', 'sleeping', 'tired']:
            return 'sleep' # Standardize to 'sleep' to match history.py stats
        
        # 2. Map ALL other emotions (happy, sad, surprise, etc.) to Neutral
        # This enforces your app's logic.
        return 'neutral'
    
    def add_emotion(self, modality, emotion, confidence=1.0):
        """Add emotion detection from a modality"""
        with self.lock:
            emotion = self.normalize_emotion(emotion) # Apply normalization
            self.recent_emotions[modality].append({
                'emotion': emotion,
                'confidence': confidence,
                'timestamp': datetime.now()
            })
            print(f"📊 Added {modality}: {emotion} (confidence: {confidence:.2f})")
    
    def get_fused_emotion(self):
        """Compute fused emotion from all modalities"""
        with self.lock:
            emotion_scores = {}
            total_weight = 0
            
            for modality, weight in self.WEIGHTS.items():
                if not self.recent_emotions[modality]:
                    continue
                
                recent = self.recent_emotions[modality][-1]
                emotion = recent['emotion']
                confidence = recent['confidence']
                score = weight * confidence
                
                if emotion in emotion_scores:
                    emotion_scores[emotion] += score
                else:
                    emotion_scores[emotion] = score
                
                total_weight += weight
            
            if not emotion_scores:
                return "neutral", 0.0, {}
            
            if total_weight > 0:
                emotion_scores = {e: s/total_weight for e, s in emotion_scores.items()}
            
            temporal_scores = self.calculate_temporal_scores()
            final_scores = {}
            for emotion in set(list(emotion_scores.keys()) + list(temporal_scores.keys())):
                current = emotion_scores.get(emotion, 0)
                temporal = temporal_scores.get(emotion, 0)
                final_scores[emotion] = 0.7 * current + 0.3 * temporal
            
            if final_scores:
                top_emotion = max(final_scores.items(), key=lambda x: x[1])
                fused_emotion = top_emotion[0]
                confidence = top_emotion[1]
                self.last_fused_emotion = fused_emotion
                self.emotion_scores = final_scores
                return fused_emotion, confidence, final_scores
            
            return self.last_fused_emotion, 0.5, {}
    
    def calculate_temporal_scores(self):
        """Calculate emotion scores based on recent history"""
        temporal_scores = {}
        
        for modality, weight in self.WEIGHTS.items():
            emotions = self.recent_emotions[modality]
            if not emotions:
                continue
            
            for i, item in enumerate(emotions):
                emotion = item['emotion']
                confidence = item['confidence']
                decay = 0.5 + (0.5 * (i / len(emotions)))
                score = weight * confidence * decay
                
                if emotion in temporal_scores:
                    temporal_scores[emotion] += score
                else:
                    temporal_scores[emotion] = score
        
        total = sum(temporal_scores.values())
        if total > 0:
            temporal_scores = {e: s/total for e, s in temporal_scores.items()}
        
        return temporal_scores
    
    def get_detailed_analysis(self):
        """Get detailed breakdown of current emotion state"""
        with self.lock:
            fused_emotion, confidence, scores = self.get_fused_emotion()
            
            modality_states = {}
            for modality in ['face', 'voice', 'text']:
                if self.recent_emotions[modality]:
                    recent = self.recent_emotions[modality][-1]
                    modality_states[modality] = {
                        'emotion': recent['emotion'],
                        'confidence': recent['confidence'],
                        'weight': self.WEIGHTS[modality]
                    }
                else:
                    modality_states[modality] = None
            
            return {
                'fused_emotion': fused_emotion,
                'confidence': confidence,
                'emotion_scores': scores,
                'modality_states': modality_states,
                'timestamp': datetime.now().isoformat()
            }
    
    def clear_modality(self, modality):
        """Clear history for a specific modality"""
        with self.lock:
            self.recent_emotions[modality].clear()
    
    def reset(self):
        """Reset all emotion history"""
        with self.lock:
            for modality in self.recent_emotions:
                self.recent_emotions[modality].clear()
            self.last_fused_emotion = "neutral"
            self.emotion_scores = {}
            print("🔄 Emotion fusion system reset")


class ContinuousFusion:
    """Continuous emotion fusion for real-time detection"""
    
    def __init__(self, callback=None, fusion_interval=2.0):
        self.fusion = EmotionFusion(temporal_window=5)
        self.callback = callback
        self.fusion_interval = fusion_interval
        self.is_running = False
        self.thread = None
        self.last_emotion = "neutral"
    
    def start(self):
        """Start continuous fusion thread"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._fusion_loop, daemon=True)
        self.thread.start()
        print("🚀 Continuous emotion fusion started")
    
    def stop(self):
        """Stop continuous fusion thread"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("⏹️ Continuous emotion fusion stopped")
    
    def _fusion_loop(self):
        """Main fusion loop"""
        
        while self.is_running:
            fused_emotion, confidence, scores = self.fusion.get_fused_emotion()
            
            if fused_emotion != self.last_emotion and confidence > 0.3:
                self.last_emotion = fused_emotion
                
                if self.callback:
                    analysis = self.fusion.get_detailed_analysis()
                    self.callback(fused_emotion, confidence, analysis)
                
                # This print is now redundant, as callback will print
                # print(f"🎯 Fused Emotion: {fused_emotion} (confidence: {confidence:.2f})")
            
            time.sleep(self.fusion_interval)
    
    def add_face_emotion(self, emotion, confidence=1.0):
        """Add face emotion detection"""
        self.fusion.add_emotion('face', emotion, confidence)
    
    def add_voice_emotion(self, emotion, confidence=1.0):
        """Add voice emotion detection"""
        self.fusion.add_emotion('voice', emotion, confidence)
    
    def add_text_emotion(self, emotion, confidence=1.0):
        """Add text emotion detection"""
        self.fusion.add_emotion('text', emotion, confidence)
# --- END OF EMOTION_FUSION.PY CODE ---


class HomePage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.camera_active = False
        self.recording_active = False
        self.camera_timer = None
        self.camera = None
        self.audio_stream = None
        self.audio_frames = []
        
        self.emotion_buffer = []
        self.buffer_start_time = None
        self.buffer_timer = None
        
        self.setup_ui()
        
        # Initialize emotion fusion
        self.emotion_fusion = ContinuousFusion(
            callback=self.on_fused_emotion_changed,
            fusion_interval=2.0
        )
        self.emotion_fusion.start()
        print("✅ Emotion fusion system initialized")
        
    def setup_ui(self):
        """EXACT SAME AS YOUR ORIGINAL - NO CHANGES"""
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Greeting Card
        greeting_card = QFrame()
        greeting_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        greeting_layout = QVBoxLayout(greeting_card)
        
        self.greeting_label = QLabel()
        self.greeting_label.setStyleSheet("""
            QLabel {
                font-size: 26px;
                color: white;
                font-weight: bold;
            }
        """)
        self.greeting_label.setAlignment(Qt.AlignCenter)
        
        self.mood_label = QLabel()
        self.mood_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: medium;
            }
        """)
        self.mood_label.setAlignment(Qt.AlignCenter)
        
        self.pet_reaction_label = QLabel()
        self.pet_reaction_label.setStyleSheet("font-size: 16px; color: #cccccc;")
        self.pet_reaction_label.setAlignment(Qt.AlignCenter)
        
        greeting_layout.addWidget(self.greeting_label)
        greeting_layout.addWidget(self.mood_label)
        greeting_layout.addWidget(self.pet_reaction_label)
        
        # Detection Controls Card
        controls_card = QFrame()
        controls_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        controls_layout = QVBoxLayout(controls_card)
        controls_layout.setSpacing(20)
        
        detection_title = QLabel("Emotion Detection")
        detection_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
            }
        """)
        
        controls_layout.addWidget(detection_title)
        
        self.setup_face_detection(controls_layout)
        self.setup_voice_detection(controls_layout)
        self.setup_text_analysis(controls_layout)
        
        layout.addWidget(greeting_card)
        layout.addWidget(controls_card)
        layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def setup_face_detection(self, layout):
        face_group = QFrame()
        face_layout = QVBoxLayout(face_group)
        face_layout.setContentsMargins(100, 0, 100, 0)
        
        face_title = QLabel("Face Analysis")
        face_title.setStyleSheet("font-size: 14px; color: #aaaaaa;")
        
        self.face_start_button = QPushButton("Start Camera")
        self.face_start_button.setIcon(QIcon(":/icons/camera.png"))
        self.face_start_button.clicked.connect(self.start_face_detection)
        
        self.face_stop_button = QPushButton("Stop")
        self.face_stop_button.setIcon(QIcon(":/icons/stop.png"))
        self.face_stop_button.setEnabled(False)
        self.face_stop_button.clicked.connect(self.stop_face_detection)
        
        self.style_buttons([self.face_start_button, self.face_stop_button])
        
        face_buttons = QHBoxLayout()
        face_buttons.setSpacing(100)
        face_buttons.addWidget(self.face_start_button)
        face_buttons.addWidget(self.face_stop_button)
        
        face_layout.addWidget(face_title)
        face_layout.addLayout(face_buttons)
        layout.addWidget(face_group)
    
    def setup_voice_detection(self, layout):
        voice_group = QFrame()
        voice_layout = QVBoxLayout(voice_group)
        voice_layout.setContentsMargins(100, 0, 100, 0)
        
        voice_title = QLabel("Voice Analysis")
        voice_title.setStyleSheet("font-size: 14px; color: #aaaaaa;")
        
        self.voice_start_button = QPushButton("Start Recording")
        self.voice_start_button.setIcon(QIcon(":/icons/microphone.png"))
        self.voice_start_button.clicked.connect(self.start_voice_detection)
        
        self.voice_stop_button = QPushButton("Stop")
        self.voice_stop_button.setIcon(QIcon(":/icons/stop.png"))
        self.voice_stop_button.setEnabled(False)
        self.voice_stop_button.clicked.connect(self.stop_voice_detection)
        
        self.style_buttons([self.voice_start_button, self.voice_stop_button])
        
        voice_buttons = QHBoxLayout()
        voice_buttons.setSpacing(100)
        voice_buttons.addWidget(self.voice_start_button)
        voice_buttons.addWidget(self.voice_stop_button)
        
        voice_layout.addWidget(voice_title)
        voice_layout.addLayout(voice_buttons)
        layout.addWidget(voice_group)
    
    def setup_text_analysis(self, layout):
        text_group = QFrame()
        text_layout = QVBoxLayout(text_group)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        text_title = QLabel("Text Analysis")
        text_title.setStyleSheet("font-size: 14px; color: #aaaaaa;")
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("How are you feeling today?")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 8px;
                padding: 4px 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #7d85a0;
            }
        """)
        
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setIcon(QIcon(":/icons/analyze.png"))
        self.analyze_button.clicked.connect(self.analyze_text)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 4px 6px;
                font-size: 14px;
                min-width: 10px;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        text_input_layout = QHBoxLayout()
        text_input_layout.setSpacing(100)
        text_input_layout.addWidget(self.text_input, 1)
        text_input_layout.addWidget(self.analyze_button)
        
        text_layout.addWidget(text_title)
        text_layout.addLayout(text_input_layout)
        layout.addWidget(text_group)
    
    def style_buttons(self, buttons):
        for btn in buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #5c6378;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 4px 6px;
                    font-size: 14px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #6c748c;
                }
                QPushButton:pressed {
                    background-color: #4a5268;
                }
                QPushButton:disabled {
                    background-color: #3a404d;
                    color: #777777;
                }
            """)
    
    # --- !!! LOGIC FIX 2: This is the new, single point of saving !!! ---
    def on_fused_emotion_changed(self, emotion, confidence, analysis):
        """Called when fused emotion changes - THIS IS THE NEW SAVE POINT"""
        print(f"🎯 Fused Emotion: {emotion} (confidence: {confidence:.1%})")
        
        # Save the *fused* emotion to history
        try:
            user_id = self.parent_window.user_id if hasattr(self.parent_window, 'user_id') else 1
            # Save as "Fused Detection" to create the common output
            APIClient.add_mood_entry(user_id, emotion, "Fused Detection") 
            print(f"✅ Saved FUSED emotion to history: {emotion}")
        except Exception as e:
            print(f"❌ Failed to save fused emotion to history: {e}")
            
        # Update the UI
        self.update_emotion(emotion)
    
    def start_emotion_buffer(self):
        """Start collecting emotions for 1 minute"""
        self.emotion_buffer = []
        self.buffer_start_time = datetime.now()
        
        self.buffer_timer = QTimer()
        self.buffer_timer.timeout.connect(self.process_emotion_buffer)
        self.buffer_timer.start(60000)  # 60 seconds
        
        print("📊 Emotion buffer started - collecting for 1 minute...")
    
    def add_emotion_to_buffer(self, emotion):
        """Add detected emotion to buffer"""
        if not self.buffer_start_time:
            self.start_emotion_buffer()
        
        self.emotion_buffer.append({
            'emotion': emotion,
            'time': datetime.now()
        })
        print(f"📝 Added to buffer: {emotion} (Total: {len(self.emotion_buffer)})")
    
    # --- !!! LOGIC FIX 3: This function NO LONGER saves to history !!! ---
    def process_emotion_buffer(self):
        """Process buffer - NOW ONLY FEEDS FUSION"""
        if not self.emotion_buffer:
            print("⚠️ No emotions in buffer")
            return
        
        emotion_counts = Counter([e['emotion'] for e in self.emotion_buffer])
        most_common_emotion, count = emotion_counts.most_common(1)[0]
        
        print(f"📊 Buffer results: {dict(emotion_counts)}")
        print(f"🎯 Most detected: {most_common_emotion} ({count} times)")
        
        # ✅ CHANGED: Add to fusion instead of direct update
        confidence = count / len(self.emotion_buffer)
        # We send the raw emotion (e.g., 'happy') to the fusion class
        # The fusion class's normalize_emotion function will handle filtering it
        self.emotion_fusion.add_face_emotion(most_common_emotion, confidence=confidence)
        
        # --- REMOVED: APIClient.add_mood_entry(...) ---
        # We no longer save the raw face buffer. The fused result is saved 
        # in on_fused_emotion_changed.
        
        self.emotion_buffer = []
        self.buffer_start_time = None
        
        if self.camera_active:
            self.start_emotion_buffer()
    
    def start_face_detection(self):
        """Start camera and face emotion detection"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                QMessageBox.warning(self, "Camera Error", "Could not access camera!")
                return
            
            self.camera_active = True
            self.face_start_button.setEnabled(False)
            self.face_stop_button.setEnabled(True)
            
            self.start_emotion_buffer()
            
            self.camera_timer = QTimer()
            self.camera_timer.timeout.connect(self.capture_and_analyze)
            self.camera_timer.start(5000)  # Every 5 seconds
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start camera: {str(e)}")
    
    def capture_and_analyze(self):
        """Capture frame and send to backend"""
        if not self.camera_active or self.camera is None:
            return
        
        try:
            ret, frame = self.camera.read()
            if not ret:
                return
            
            _, buffer = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            result = APIClient.predict_face_emotion(image_base64)
            
            if 'error' in result:
                print(f"Face detection error: {result['error']}")
            elif 'emotion' in result:
                emotion = result['emotion'].lower()
                self.add_emotion_to_buffer(emotion)
                
        except Exception as e:
            print(f"Capture error: {str(e)}")
    
    def stop_face_detection(self):
        """Stop camera"""
        self.camera_active = False
        
        if self.buffer_timer:
            self.buffer_timer.stop()
            self.buffer_timer = None
        
        if self.camera_timer:
            self.camera_timer.stop()
            self.camera_timer = None
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        if self.emotion_buffer:
            self.process_emotion_buffer()
        
        self.face_start_button.setEnabled(True)
        self.face_stop_button.setEnabled(False)
    
    def start_voice_detection(self):
        """Start recording audio"""
        try:
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=22050,
                input=True,
                frames_per_buffer=1024
            )
            
            self.recording_active = True
            self.audio_frames = []
            self.voice_start_button.setEnabled(False)
            self.voice_stop_button.setEnabled(True)
            
            self.record_timer = QTimer()
            self.record_timer.timeout.connect(self.record_audio_chunk)
            self.record_timer.start(100)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start recording: {str(e)}")
    
    def record_audio_chunk(self):
        """Record audio chunk"""
        if not self.recording_active:
            return
        
        try:
            data = self.audio_stream.read(1024, exception_on_overflow=False)
            self.audio_frames.append(data)
        except Exception as e:
            print(f"Recording error: {str(e)}")
    
    def stop_voice_detection(self):
        """Stop recording and analyze"""
        self.recording_active = False
        
        if self.record_timer:
            self.record_timer.stop()
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        
        if hasattr(self, 'audio'):
            self.audio.terminate()
        
        self.voice_start_button.setEnabled(True)
        self.voice_stop_button.setEnabled(False)
        
        if self.audio_frames:
            self.process_audio()
    
    def process_audio(self):
        """Convert audio to base64 and send to backend"""
        try:
            wav_io = io.BytesIO()
            with wave.open(wav_io, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(22050)
                wf.writeframes(b''.join(self.audio_frames))
            
            audio_base64 = base64.b64encode(wav_io.getvalue()).decode('utf-8')
            result = APIClient.predict_voice_emotion(audio_base64)
            
            if 'error' in result:
                QMessageBox.warning(self, "Error", f"Voice analysis failed: {result['error']}")
            elif 'emotion' in result:
                emotion = result['emotion'].lower()
                # ✅ CHANGED: Add to fusion
                self.emotion_fusion.add_voice_emotion(emotion, confidence=0.85)
                print(f"🎤 Voice detected: {emotion}")
                # We show the raw detection, but the *fused* emotion will be saved
                QMessageBox.information(self, "Voice Analysis", f"Detected emotion: {emotion.capitalize()}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process audio: {str(e)}")
    
    def analyze_text(self):
        """Analyze text emotion"""
        text = self.text_input.text().strip()
        
        if not text:
            QMessageBox.warning(self, "Input Required", "Please enter some text to analyze!")
            return
        
        try:
            result = APIClient.predict_text_emotion(text)
            
            if 'error' in result:
                QMessageBox.warning(self, "Error", f"Text analysis failed: {result['error']}")
            elif 'emotion' in result:
                emotion = result['emotion'].lower()
                # ✅ CHANGED: Add to fusion
                self.emotion_fusion.add_text_emotion(emotion, confidence=0.7)
                print(f"📝 Text detected: {emotion}")
                # We show the raw detection, but the *fused* emotion will be saved
                QMessageBox.information(self, "Text Analysis", f"Detected emotion: {emotion.capitalize()}")
                self.text_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to analyze text: {str(e)}")
    
    # --- !!! LOGIC FIX 4: Pet reactions must match 4 emotions !!! ---
    def update_emotion(self, emotion):
        """Update UI with detected emotion"""
        if hasattr(self.parent_window, 'current_mood'):
            self.parent_window.current_mood = emotion
        
        self.update_mood(emotion)
        
        if hasattr(self.parent_window, 'pet_page'):
            # Use only your 4 target emotions
            pet_reactions = {
                "angry": "angry",
                "stress": "sad",     # Stress makes pet sad
                "neutral": "neutral", # Neutral pet
                "sleep": "sleepy"     # Sleep makes pet sleepy
            }
            # Default to "neutral" if emotion is not in map
            pet_mood = pet_reactions.get(emotion, "neutral") 
            
            self.parent_window.pet_page.pet_mood = pet_mood
            
            if hasattr(self.parent_window.pet_page, 'update_ui'):
                self.parent_window.pet_page.update_ui()
            
            try:
                user_id = self.parent_window.user_id if hasattr(self.parent_window, 'user_id') else 1
                APIClient.update_pet_mood(user_id, pet_mood)
            except Exception as e:
                print(f"Failed to update pet mood: {e}")
    
    def update_content(self, username, mood, pet_name):
        self.update_username(username)
        self.update_mood(mood)
    
    def update_username(self, username):
        self.greeting_label.setText(f"Hello, {username}! 👋")
    
    # --- !!! LOGIC FIX 5: UI must match 4 emotions !!! ---
    def update_mood(self, mood):
        # Use only your 4 target emotions
        mood_colors = {
            "angry": "#FF4500",
            "stress": "#FF6347",
            "neutral": "#FFFFFF",
            "sleep": "#9370DB"
        }
        self.mood_label.setText(f"Current Mood: {mood.capitalize()}")
        self.mood_label.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: medium;
                color: {mood_colors.get(mood, '#FFFFFF')};
            }}
        """)
        
        # Use only your 4 target emotions
        reactions = {
            "angry": "Your pet is trying to calm you down",
            "stress": "Your pet wants to help you relax",
            "neutral": "Your pet is peacefully resting",
            "sleep": "Your pet is feeling sleepy too"
        }
        self.pet_reaction_label.setText(reactions.get(mood, "Your pet is peacefully resting"))
    
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'emotion_fusion'):
            self.emotion_fusion.stop()
            print("✅ Emotion fusion stopped")
        
        if self.camera_active:
            self.stop_face_detection()
        if self.recording_active:
            self.stop_voice_detection()
        if self.buffer_timer:
            self.buffer_timer.stop()