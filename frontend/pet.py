from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt
import random

class PetPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.animation_frames = {
            "happy": ["🐇", "🐰", "😊", "😄"],
            "sad": ["😢", "😞", "💧", "😔"],
            "angry": ["😠", "👿", "💢", "🤬"],
            "neutral": ["🐾", "🦔", "😐", "🙂"]
        }
        self.current_frame = 0
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        # Pet Animation Card
        animation_card = QFrame()
        animation_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        animation_layout = QVBoxLayout(animation_card)
        animation_layout.setAlignment(Qt.AlignCenter)
        
        self.pet_animation_label = QLabel()
        self.pet_animation_label.setStyleSheet("font-size: 72px;")
        self.pet_animation_label.setAlignment(Qt.AlignCenter)
        
        self.pet_mood_label = QLabel()
        self.pet_mood_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: white;
                font-weight: medium;
            }
        """)
        self.pet_mood_label.setAlignment(Qt.AlignCenter)
        
        animation_layout.addWidget(self.pet_animation_label)
        animation_layout.addWidget(self.pet_mood_label)
        
        # Pet Stats Card
        stats_card = QFrame()
        stats_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        
        stats_layout = QVBoxLayout(stats_card)
        
        stats_title = QLabel("Pet Stats")
        stats_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)
        
        self.happiness_label = QLabel("Happiness: 80%")
        self.energy_label = QLabel("Energy: 65%")
        self.hunger_label = QLabel("Hunger: 30%")
        
        for label in [self.happiness_label, self.energy_label, self.hunger_label]:
            label.setStyleSheet("font-size: 16px; color: #cccccc;")
        
        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(self.happiness_label)
        stats_layout.addWidget(self.energy_label)
        stats_layout.addWidget(self.hunger_label)
        
        layout.addWidget(animation_card)
        layout.addWidget(stats_card)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def update_content(self, pet_name, pet_mood):
        self.pet_name = pet_name
        self.pet_mood = pet_mood
        self.update_mood()
    
    def update_mood(self, mood=None):
        if mood:
            self.pet_mood = mood
        self.pet_mood_label.setText(f"{self.pet_name}'s Mood: {self.pet_mood.capitalize()}")
    
    def animate(self):
        frames = self.animation_frames.get(self.pet_mood, ["🐾"])
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.pet_animation_label.setText(frames[self.current_frame])