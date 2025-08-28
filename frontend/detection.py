from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem)
from PySide6.QtGui import QIcon

class DetectionPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Emotion Detection")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Detection Methods Card
        methods_card = QFrame()
        methods_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        methods_layout = QVBoxLayout(methods_card)
        methods_layout.setSpacing(20)
        
        # Face Detection
        face_group = self.create_detection_group(
            "Face Detection", 
            "Detect emotions from your facial expressions using your camera",
            ":/icons/camera.png"
        )
        
        # Voice Detection
        voice_group = self.create_detection_group(
            "Voice Analysis", 
            "Analyze your emotional state from voice tone and speech patterns",
            ":/icons/microphone.png"
        )
        
        # Text Analysis
        text_group = self.create_detection_group(
            "Text Analysis", 
            "Understand your mood from written text or transcribed speech",
            ":/icons/text.png"
        )
        
        methods_layout.addWidget(face_group)
        methods_layout.addWidget(voice_group)
        methods_layout.addWidget(text_group)
        
        layout.addWidget(methods_card)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def create_detection_group(self, title, description, icon_path):
        group = QFrame()
        group.setStyleSheet("""
            QFrame {
                background-color: #5c6378;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        # Title row
        title_layout = QHBoxLayout()
        
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
            }
        """)
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        desc_label.setWordWrap(True)
        
        # Button
        start_button = QPushButton(f"Start {title.split()[0]} Detection")
        start_button.setIcon(QIcon(":/icons/play.png"))
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        layout.addLayout(title_layout)
        layout.addWidget(desc_label)
        layout.addWidget(start_button)
        
        return group