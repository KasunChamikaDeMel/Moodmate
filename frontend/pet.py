

from PySide6.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QProgressBar, QSizePolicy, QSpacerItem, QMessageBox)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QPainter, QColor, QPen
from datetime import datetime, timedelta
import random
from api_client import APIClient

class PetWidget(QFrame):
    """Custom animated pet widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.pet_mood = "happy"
        self.animation_frame = 0
        self.bounce_offset = 0
        
        # Animation timer
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(100)
    
    def set_mood(self, mood):
        """Update pet mood"""
        self.pet_mood = mood.lower()
        self.update()
    
    def update_animation(self):
        """Update animation frame"""
        self.animation_frame = (self.animation_frame + 1) % 30
        self.bounce_offset = abs((self.animation_frame % 20) - 10) * 2
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event for pet"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate center position with bounce
        center_x = self.width() // 2
        center_y = self.height() // 2 - self.bounce_offset
        
        # Mood-based colors and expressions
        mood_config = {
            "happy": {"body": "#FFD700", "accent": "#FFA500", "face": "^_^"},
            "sad": {"body": "#87CEEB", "accent": "#4682B4", "face": "T_T"},
            "angry": {"body": "#FF6347", "accent": "#DC143C", "face": ">_<"},
            "stress": {"body": "#FF8C00", "accent": "#FF4500", "face": "@_@"},
            "sleepy": {"body": "#9370DB", "accent": "#8A2BE2", "face": "-_-"},
            "neutral": {"body": "#98FB98", "accent": "#3CB371", "face": "o_o"}
        }
        
        config = mood_config.get(self.pet_mood, mood_config["neutral"])
        
        # Draw body (circle)
        body_color = QColor(config["body"])
        painter.setBrush(body_color)
        painter.setPen(QPen(QColor(config["accent"]), 3))
        body_size = 80
        painter.drawEllipse(center_x - body_size//2, center_y - body_size//2, 
                          body_size, body_size)
        
        # Draw ears (triangles)
        ear_size = 30
        painter.setBrush(QColor(config["accent"]))
        # Left ear
        painter.drawPolygon([
            QPoint(center_x - body_size//3, center_y - body_size//2),
            QPoint(center_x - body_size//3 - ear_size//2, center_y - body_size//2 - ear_size),
            QPoint(center_x - body_size//3 + ear_size//2, center_y - body_size//2 - ear_size//2)
        ])
        # Right ear
        painter.drawPolygon([
            QPoint(center_x + body_size//3, center_y - body_size//2),
            QPoint(center_x + body_size//3 - ear_size//2, center_y - body_size//2 - ear_size//2),
            QPoint(center_x + body_size//3 + ear_size//2, center_y - body_size//2 - ear_size)
        ])
        
        # Draw face
        painter.setPen(QPen(Qt.black, 2))
        font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(font)
        face_rect = painter.boundingRect(0, 0, 0, 0, Qt.AlignCenter, config["face"])
        painter.drawText(center_x - face_rect.width()//2, 
                        center_y - face_rect.height()//2,
                        config["face"])
        
        # Draw name tag
        name_font = QFont("Arial", 10)
        painter.setFont(name_font)
        painter.setPen(QPen(Qt.white, 1))
        if hasattr(self.parent(), 'pet_name'):
            painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, 
                           self.parent().pet_name)


class PetPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.pet_name = "Buddy"
        self.pet_mood = "happy"
        self.pet_level = 1
        self.pet_exp = 0
        self.happiness = 80
        self.energy = 65
        self.hunger = 30
        self.last_interaction = datetime.now()
        
        self.setup_ui()
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_pet_stats)
        self.update_timer.start(60000)  # Update every minute
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel(f"Your Pet: {self.pet_name}")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                color: white;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Pet Widget Container
        pet_container = QFrame()
        pet_container.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        pet_layout = QVBoxLayout(pet_container)
        
        # Animated Pet
        self.pet_widget = PetWidget(self)
        pet_widget_container = QHBoxLayout()
        pet_widget_container.addStretch()
        pet_widget_container.addWidget(self.pet_widget)
        pet_widget_container.addStretch()
        pet_layout.addLayout(pet_widget_container)
        
        # Mood Label
        self.mood_label = QLabel(f"Mood: {self.pet_mood.capitalize()}")
        self.mood_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #FFD700;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.mood_label.setAlignment(Qt.AlignCenter)
        pet_layout.addWidget(self.mood_label)
        
        # Level and EXP
        level_layout = QHBoxLayout()
        self.level_label = QLabel(f"Level: {self.pet_level}")
        self.level_label.setStyleSheet("font-size: 16px; color: white;")
        
        self.exp_bar = QProgressBar()
        self.exp_bar.setMaximum(100)
        self.exp_bar.setValue(self.pet_exp)
        self.exp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #5c6378;
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: #2a2f3a;
            }
            QProgressBar::chunk {
                background-color: #6c5ce7;
                border-radius: 3px;
            }
        """)
        
        level_layout.addWidget(self.level_label)
        level_layout.addWidget(self.exp_bar, 1)
        pet_layout.addLayout(level_layout)
        
        layout.addWidget(pet_container)
        
        # Stats Card
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
                font-size: 20px;
                color: white;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)
        stats_layout.addWidget(stats_title)
        
        # Happiness Bar
        self.happiness_bar = self.create_stat_bar("Happiness", self.happiness, "#FFD700")
        stats_layout.addLayout(self.happiness_bar)
        
        # Energy Bar
        self.energy_bar = self.create_stat_bar("Energy", self.energy, "#4CAF50")
        stats_layout.addLayout(self.energy_bar)
        
        # Hunger Bar
        self.hunger_bar = self.create_stat_bar("Hunger", self.hunger, "#FF6347")
        stats_layout.addLayout(self.hunger_bar)
        
        layout.addWidget(stats_card)
        
        # Interaction Buttons
        button_card = QFrame()
        button_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        button_layout = QHBoxLayout(button_card)
        
        self.feed_btn = self.create_action_button("🍎 Feed", "#4CAF50")
        self.play_btn = self.create_action_button("🎾 Play", "#2196F3")
        self.sleep_btn = self.create_action_button("😴 Sleep", "#9C27B0")
        
        self.feed_btn.clicked.connect(self.feed_pet)
        self.play_btn.clicked.connect(self.play_with_pet)
        self.sleep_btn.clicked.connect(self.pet_sleep)
        
        button_layout.addWidget(self.feed_btn)
        button_layout.addWidget(self.play_btn)
        button_layout.addWidget(self.sleep_btn)
        
        layout.addWidget(button_card)
        layout.addStretch()
    
    def create_stat_bar(self, label, value, color):
        """Create a stat bar with label"""
        layout = QVBoxLayout()
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        bar = QProgressBar()
        bar.setMaximum(100)
        bar.setValue(value)
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #5c6378;
                border-radius: 5px;
                text-align: center;
                color: white;
                background-color: #2a2f3a;
                height: 25px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        
        # Store reference for updates
        if label == "Happiness":
            self.happiness_progress = bar
        elif label == "Energy":
            self.energy_progress = bar
        elif label == "Hunger":
            self.hunger_progress = bar
        
        layout.addWidget(label_widget)
        layout.addWidget(bar)
        return layout
    
    def create_action_button(self, text, color):
        """Create an action button"""
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}bb;
            }}
        """)
        return btn
    
    def feed_pet(self):
        """Feed the pet"""
        try:
            result = APIClient.feed_pet(1)
            if 'error' not in result:
                self.hunger = max(0, self.hunger - 20)
                self.happiness = min(100, self.happiness + 10)
                self.pet_exp = min(100, self.pet_exp + 5)
                self.update_stats_display()
                self.update_mood("happy")
                QMessageBox.information(self, "Success", f"{self.pet_name} enjoyed the food! 🍎")
            else:
                QMessageBox.warning(self, "Error", f"Feeding failed: {result['error']}")
        except Exception as e:
            # Offline mode
            self.hunger = max(0, self.hunger - 20)
            self.happiness = min(100, self.happiness + 10)
            self.update_stats_display()
            self.update_mood("happy")
    
    def play_with_pet(self):
        """Play with the pet"""
        if self.energy < 20:
            QMessageBox.warning(self, "Too Tired", 
                              f"{self.pet_name} is too tired to play! Let them rest.")
            return
        
        self.energy = max(0, self.energy - 15)
        self.happiness = min(100, self.happiness + 20)
        self.hunger = min(100, self.hunger + 10)
        self.pet_exp = min(100, self.pet_exp + 10)
        self.update_stats_display()
        self.update_mood("happy")
        
        activities = [
            "loves playing fetch!",
            "is having so much fun!",
            "is jumping with joy!",
            "really enjoyed that!"
        ]
        QMessageBox.information(self, "Play Time", 
                               f"{self.pet_name} {random.choice(activities)} 🎾")
    
    def pet_sleep(self):
        """Let pet sleep"""
        self.energy = min(100, self.energy + 30)
        self.hunger = min(100, self.hunger + 5)
        self.update_stats_display()
        self.update_mood("sleepy")
        QMessageBox.information(self, "Rest Time", 
                               f"{self.pet_name} is taking a nap... 😴")
    
    def update_mood(self, mood):
        """Update pet mood"""
        self.pet_mood = mood
        self.mood_label.setText(f"Mood: {self.pet_mood.capitalize()}")
        self.pet_widget.set_mood(mood)
        
        # Update backend
        try:
            APIClient.update_pet_mood(1, mood)
        except:
            pass  # Offline mode
    
    def update_stats_display(self):
        """Update all stat displays"""
        self.happiness_progress.setValue(self.happiness)
        self.energy_progress.setValue(self.energy)
        self.hunger_progress.setValue(self.hunger)
        self.exp_bar.setValue(self.pet_exp)
        
        # Check level up
        if self.pet_exp >= 100:
            self.level_up()
    
    def level_up(self):
        """Level up the pet"""
        self.pet_level += 1
        self.pet_exp = 0
        self.level_label.setText(f"Level: {self.pet_level}")
        QMessageBox.information(self, "Level Up!", 
                               f"🎉 {self.pet_name} reached level {self.pet_level}!")
    
    def update_pet_stats(self):
        """Periodic stat decay"""
        time_since_interaction = datetime.now() - self.last_interaction
        minutes_passed = time_since_interaction.total_seconds() / 60
        
        if minutes_passed > 5:
            self.hunger = min(100, self.hunger + 2)
            self.energy = max(0, self.energy - 1)
            self.happiness = max(0, self.happiness - 1)
            self.update_stats_display()
            
            # Auto mood update based on stats
            if self.hunger > 80:
                self.update_mood("angry")
            elif self.energy < 20:
                self.update_mood("sleepy")
            elif self.happiness < 30:
                self.update_mood("sad")
    
    def update_content(self, pet_name, pet_mood):
        """Update from parent window"""
        self.pet_name = pet_name
        self.update_mood(pet_mood)
    
    def refresh_data(self):
        """Refresh pet data from backend"""
        try:
            result = APIClient.get_pet_data(1)
            if 'error' not in result:
                self.pet_name = result.get('pet_name', 'Buddy')
                self.pet_mood = result.get('pet_mood', 'happy')
                self.pet_level = result.get('pet_level', 1)
                self.pet_exp = result.get('pet_exp', 0)
                self.update_stats_display()
                self.update_mood(self.pet_mood)
        except Exception as e:
            print(f"Failed to refresh pet data: {e}")