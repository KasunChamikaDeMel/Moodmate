"""
Home Page with Backend Integration
Handles face, voice, and text emotion detection
"""

from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                              QLineEdit, QSizePolicy, QSpacerItem, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
import cv2
import base64
import pyaudio
import wave
import io
from api_client import APIClient

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
        self.setup_ui()
        
    def setup_ui(self):
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
        
        # Detection title
        detection_title = QLabel("Emotion Detection")
        detection_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
            }
        """)
        
        controls_layout.addWidget(detection_title)
        
        # Face detection controls
        self.setup_face_detection(controls_layout)
        
        # Voice detection controls
        self.setup_voice_detection(controls_layout)
        
        # Text analysis controls
        self.setup_text_analysis(controls_layout)
        
        # Add cards to main layout
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
    
    # ==================== FACE DETECTION ====================
    
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
            
            # Timer to capture frames
            self.camera_timer = QTimer()
            self.camera_timer.timeout.connect(self.capture_and_analyze)
            self.camera_timer.start(3000)  # Analyze every 3 seconds
            
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
            
            # Encode frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Send to backend
            result = APIClient.predict_face_emotion(image_base64)
            
            if 'error' in result:
                print(f"Face detection error: {result['error']}")
            elif 'emotion' in result:
                emotion = result['emotion'].lower()
                self.update_emotion(emotion)
                
        except Exception as e:
            print(f"Capture error: {str(e)}")
    
    def stop_face_detection(self):
        """Stop camera"""
        self.camera_active = False
        
        if self.camera_timer:
            self.camera_timer.stop()
            self.camera_timer = None
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        self.face_start_button.setEnabled(True)
        self.face_stop_button.setEnabled(False)
    
    # ==================== VOICE DETECTION ====================
    
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
            
            # Start recording timer
            self.record_timer = QTimer()
            self.record_timer.timeout.connect(self.record_audio_chunk)
            self.record_timer.start(100)  # Record chunks every 100ms
            
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
        
        # Process recorded audio
        if self.audio_frames:
            self.process_audio()
    
    def process_audio(self):
        """Convert audio to base64 and send to backend"""
        try:
            # Create WAV file in memory
            wav_io = io.BytesIO()
            with wave.open(wav_io, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(22050)
                wf.writeframes(b''.join(self.audio_frames))
            
            # Encode to base64
            audio_base64 = base64.b64encode(wav_io.getvalue()).decode('utf-8')
            
            # Send to backend
            result = APIClient.predict_voice_emotion(audio_base64)
            
            if 'error' in result:
                QMessageBox.warning(self, "Error", f"Voice analysis failed: {result['error']}")
            elif 'emotion' in result:
                emotion = result['emotion'].lower()
                self.update_emotion(emotion)
                QMessageBox.information(self, "Voice Analysis", f"Detected emotion: {emotion.capitalize()}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process audio: {str(e)}")
    
    # ==================== TEXT ANALYSIS ====================
    
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
                self.update_emotion(emotion)
                QMessageBox.information(self, "Text Analysis", f"Detected emotion: {emotion.capitalize()}")
                self.text_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to analyze text: {str(e)}")
    
    # ==================== UI UPDATE ====================
    
    def update_emotion(self, emotion):
        """Update UI with detected emotion"""
        if hasattr(self.parent_window, 'current_mood'):
            self.parent_window.current_mood = emotion
        
        self.update_mood(emotion)
        
        # Update pet mood
        if hasattr(self.parent_window, 'pet_page'):
            pet_reactions = {
                "happy": "happy",
                "sad": "sad",
                "angry": "angry",
                "stress": "sad",
                "neutral": "happy",
                "sleepy": "neutral"
            }
            pet_mood = pet_reactions.get(emotion, "happy")
            self.parent_window.pet_page.update_mood(pet_mood)
            
            # Update pet mood in backend
            APIClient.update_pet_mood(1, pet_mood)
    
    def update_content(self, username, mood, pet_name):
        self.update_username(username)
        self.update_mood(mood)
    
    def update_username(self, username):
        self.greeting_label.setText(f"Hello, {username}! 👋")
    
    def update_mood(self, mood):
        mood_colors = {
            "happy": "#FFD700",
            "sad": "#1E90FF",
            "angry": "#FF4500",
            "stress": "#FF6347",
            "neutral": "#FFFFFF",
            "sleepy": "#9370DB"
        }
        self.mood_label.setText(f"Current Mood: {mood.capitalize()}")
        self.mood_label.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: medium;
                color: {mood_colors.get(mood, '#FFFFFF')};
            }}
        """)
        
        reactions = {
            "happy": "Your pet is excited to see you happy!",
            "sad": "Your pet is giving you comforting cuddles",
            "angry": "Your pet is trying to calm you down",
            "stress": "Your pet wants to help you relax",
            "neutral": "Your pet is peacefully resting",
            "sleepy": "Your pet is feeling sleepy too"
        }
        self.pet_reaction_label.setText(reactions.get(mood, ""))
    
    def cleanup(self):
        """Cleanup resources when page is closed"""
        if self.camera_active:
            self.stop_face_detection()
        if self.recording_active:
            self.stop_voice_detection()