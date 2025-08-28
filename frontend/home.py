from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class HomePage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        
        # Face detection controls
        self.setup_face_detection(controls_layout)
        
        # Voice detection controls
        self.setup_voice_detection(controls_layout)
        
        # Text analysis controls
        self.setup_text_analysis(controls_layout)
        
        controls_layout.addWidget(detection_title)
        
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
        self.face_stop_button = QPushButton("Stop")
        self.face_stop_button.setIcon(QIcon(":/icons/stop.png"))
        self.face_stop_button.setEnabled(False)
        
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
        self.voice_stop_button = QPushButton("Stop")
        self.voice_stop_button.setIcon(QIcon(":/icons/stop.png"))
        self.voice_stop_button.setEnabled(False)
        
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
            "neutral": "#FFFFFF"
        }
        self.mood_label.setText(f"Current Mood: {mood.capitalize()}")
        self.mood_label.setStyleSheet(f"""
            QLabel {{
                color: {mood_colors.get(mood, '#FFFFFF')};
            }}
        """)
        
        reactions = {
            "happy": "Your pet is excited to see you happy!",
            "sad": "Your pet is giving you comforting cuddles",
            "angry": "Your pet is trying to calm you down",
            "neutral": "Your pet is peacefully resting"
        }
        self.pet_reaction_label.setText(reactions.get(mood, ""))