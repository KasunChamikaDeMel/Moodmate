"""
Beautiful Pet Page with Customization
Better visual design and pet customization options
"""

from PySide6.QtWidgets import (QFrame, QLabel, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QProgressBar, QMessageBox, QGridLayout,
                              QWidget, QButtonGroup, QRadioButton, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
# Replace line 10 with these:
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient, QRadialGradient, QPainterPath
from PySide6.QtCore import QPointF
from datetime import datetime, timedelta
import random
import math
from api_client import APIClient


class BeautifulPetWidget(QWidget):
    """Much better looking pet with smooth animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(250, 250)
        self.pet_type = "cat"
        self.pet_mood = "happy"
        self.pet_color = QColor(255, 215, 0)  # Gold
        
        # Animation
        self.time = 0
        self.bounce = 0
        self.blink = False
        self.blink_timer = 0
        self.particles = []
        self.hearts = []
        
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(50)
    
    def set_pet_type(self, pet_type):
        self.pet_type = pet_type
        self.update()
    
    def set_mood(self, mood):
        self.pet_mood = mood
        self.update()
    
    def set_color(self, color):
        self.pet_color = color
        self.update()
    
    def animate(self):
        self.time += 0.05
        self.bounce = abs(math.sin(self.time * 2)) * 8
        
        # Blinking
        self.blink_timer += 1
        if self.blink_timer > 80:
            self.blink = True
            if self.blink_timer > 85:
                self.blink = False
                self.blink_timer = 0
        
        # Hearts when happy
        if self.pet_mood == "happy" and random.random() < 0.05:
            self.hearts.append({
                'x': random.randint(-30, 30),
                'y': 30,
                'life': 50
            })
        
        # Update hearts
        self.hearts = [h for h in self.hearts if h['life'] > 0]
        for h in self.hearts:
            h['life'] -= 1
            h['y'] -= 1
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx = self.width() / 2
        cy = self.height() / 2 - self.bounce + 10
        
        # Background glow
        glow = QRadialGradient(cx, cy, 100)
        glow.setColorAt(0, QColor(self.pet_color.red(), self.pet_color.green(), 
                                   self.pet_color.blue(), 30))
        glow.setColorAt(1, QColor(self.pet_color.red(), self.pet_color.green(), 
                                   self.pet_color.blue(), 0))
        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), 110, 110)
        
        # Shadow
        shadow = QRadialGradient(cx, cy + 70, 40)
        shadow.setColorAt(0, QColor(0, 0, 0, 60))
        shadow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(shadow)
        painter.drawEllipse(QPointF(cx, cy + 70), 50, 12)
        
        # Draw pet
        if self.pet_type == "cat":
            self.draw_cat(painter, cx, cy)
        elif self.pet_type == "dog":
            self.draw_dog(painter, cx, cy)
        else:
            self.draw_bunny(painter, cx, cy)
        
        # Draw hearts
        for h in self.hearts:
            alpha = int((h['life'] / 50) * 255)
            painter.setPen(QPen(QColor(255, 105, 180, alpha), 2))
            painter.setBrush(QColor(255, 182, 193, alpha))
            heart_x = cx + h['x']
            heart_y = cy - h['y']
            self.draw_heart(painter, heart_x, heart_y, 8)
    
    def draw_cat(self, painter, cx, cy):
        # Body with gradient
        gradient = QRadialGradient(cx, cy, 50)
        gradient.setColorAt(0, self.pet_color.lighter(120))
        gradient.setColorAt(0.7, self.pet_color)
        gradient.setColorAt(1, self.pet_color.darker(110))
        
        painter.setBrush(gradient)
        painter.setPen(QPen(self.pet_color.darker(130), 3))
        painter.drawEllipse(QPointF(cx, cy), 45, 52)
        
        # Ears
        painter.setBrush(self.pet_color)
        painter.drawPolygon([
            QPointF(cx - 28, cy - 45),
            QPointF(cx - 38, cy - 70),
            QPointF(cx - 18, cy - 52)
        ])
        painter.drawPolygon([
            QPointF(cx + 28, cy - 45),
            QPointF(cx + 38, cy - 70),
            QPointF(cx + 18, cy - 52)
        ])
        
        # Inner ears (pink)
        painter.setBrush(QColor(255, 182, 193))
        painter.drawPolygon([
            QPointF(cx - 28, cy - 45),
            QPointF(cx - 32, cy - 58),
            QPointF(cx - 23, cy - 50)
        ])
        painter.drawPolygon([
            QPointF(cx + 28, cy - 45),
            QPointF(cx + 32, cy - 58),
            QPointF(cx + 23, cy - 50)
        ])
        
        # Eyes
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        if not self.blink:
            painter.drawEllipse(QPointF(cx - 18, cy - 20), 11, 14)
            painter.drawEllipse(QPointF(cx + 18, cy - 20), 11, 14)
            
            # Pupils
            painter.setBrush(Qt.black)
            painter.drawEllipse(QPointF(cx - 18, cy - 18), 6, 9)
            painter.drawEllipse(QPointF(cx + 18, cy - 18), 6, 9)
            
            # Sparkle
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPointF(cx - 15, cy - 22), 3, 3)
            painter.drawEllipse(QPointF(cx + 21, cy - 22), 3, 3)
        else:
            painter.setPen(QPen(Qt.black, 3))
            painter.drawLine(int(cx - 22), int(cy - 20), int(cx - 14), int(cy - 20))
            painter.drawLine(int(cx + 14), int(cy - 20), int(cx + 22), int(cy - 20))
        
        # Nose
        painter.setBrush(QColor(255, 105, 180))
        painter.setPen(Qt.NoPen)
        path = QPainterPath()
        path.moveTo(cx, cy - 8)
        path.lineTo(cx - 5, cy - 15)
        path.lineTo(cx + 5, cy - 15)
        path.closeSubpath()
        painter.drawPath(path)
        
        # Mouth
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap))
        if self.pet_mood == "happy":
            path = QPainterPath()
            path.moveTo(cx - 15, cy - 5)
            path.quadTo(cx, cy + 5, cx + 15, cy - 5)
            painter.drawPath(path)
        
        # Whiskers
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(int(cx - 30), int(cy - 10), int(cx - 50), int(cy - 15))
        painter.drawLine(int(cx - 30), int(cy - 5), int(cx - 50), int(cy - 5))
        painter.drawLine(int(cx - 30), int(cy), int(cx - 50), int(cy + 5))
        painter.drawLine(int(cx + 30), int(cy - 10), int(cx + 50), int(cy - 15))
        painter.drawLine(int(cx + 30), int(cy - 5), int(cx + 50), int(cy - 5))
        painter.drawLine(int(cx + 30), int(cy), int(cx + 50), int(cy + 5))
    
    def draw_dog(self, painter, cx, cy):
        # Similar to cat but with dog features
        gradient = QRadialGradient(cx, cy, 50)
        gradient.setColorAt(0, self.pet_color.lighter(120))
        gradient.setColorAt(0.7, self.pet_color)
        gradient.setColorAt(1, self.pet_color.darker(110))
        
        painter.setBrush(gradient)
        painter.setPen(QPen(self.pet_color.darker(130), 3))
        painter.drawEllipse(QPointF(cx, cy), 45, 52)
        
        # Floppy ears
        painter.setBrush(self.pet_color.darker(110))
        painter.drawEllipse(QPointF(cx - 45, cy - 20), 15, 35)
        painter.drawEllipse(QPointF(cx + 45, cy - 20), 15, 35)
        
        # Snout
        painter.setBrush(self.pet_color.lighter(110))
        painter.drawEllipse(QPointF(cx, cy + 5), 22, 18)
        
        # Eyes (similar to cat)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        if not self.blink:
            painter.drawEllipse(QPointF(cx - 18, cy - 20), 11, 14)
            painter.drawEllipse(QPointF(cx + 18, cy - 20), 11, 14)
            painter.setBrush(Qt.black)
            painter.drawEllipse(QPointF(cx - 18, cy - 18), 6, 9)
            painter.drawEllipse(QPointF(cx + 18, cy - 18), 6, 9)
        
        # Nose
        painter.setBrush(Qt.black)
        painter.drawEllipse(QPointF(cx, cy + 12), 7, 6)
    
    def draw_bunny(self, painter, cx, cy):
        gradient = QRadialGradient(cx, cy, 50)
        gradient.setColorAt(0, self.pet_color.lighter(120))
        gradient.setColorAt(0.7, self.pet_color)
        gradient.setColorAt(1, self.pet_color.darker(110))
        
        painter.setBrush(gradient)
        painter.setPen(QPen(self.pet_color.darker(130), 3))
        painter.drawEllipse(QPointF(cx, cy), 45, 50)
        
        # Long ears
        painter.setBrush(self.pet_color)
        painter.drawEllipse(QPointF(cx - 22, cy - 70), 13, 45)
        painter.drawEllipse(QPointF(cx + 22, cy - 70), 13, 45)
        
        # Inner ears
        painter.setBrush(QColor(255, 182, 193))
        painter.drawEllipse(QPointF(cx - 22, cy - 65), 7, 30)
        painter.drawEllipse(QPointF(cx + 22, cy - 65), 7, 30)
        
        # Eyes
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        if not self.blink:
            painter.drawEllipse(QPointF(cx - 18, cy - 20), 11, 16)
            painter.drawEllipse(QPointF(cx + 18, cy - 20), 11, 16)
            painter.setBrush(Qt.black)
            painter.drawEllipse(QPointF(cx - 18, cy - 18), 6, 10)
            painter.drawEllipse(QPointF(cx + 18, cy - 18), 6, 10)
        
        # Nose
        painter.setBrush(QColor(255, 105, 180))
        painter.drawEllipse(QPointF(cx, cy - 8), 5, 4)
    
    def draw_heart(self, painter, cx, cy, size):
        path = QPainterPath()
        path.moveTo(cx, cy + size/2)
        path.cubicTo(cx - size, cy - size/2, cx - size/2, cy - size, cx, cy - size/4)
        path.cubicTo(cx + size/2, cy - size, cx + size, cy - size/2, cx, cy + size/2)
        painter.drawPath(path)


class PetPage(QFrame):
    """Pet page with better design and customization"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.user_id = 1
        
        self.pet_name = "Buddy"
        self.pet_type = "cat"
        self.pet_mood = "happy"
        self.pet_color = QColor(255, 215, 0)
        self.pet_level = 1
        self.pet_exp = 0
        self.happiness = 80
        self.energy = 65
        self.hunger = 30
        self.health = 100
        self.cleanliness = 85
        self.intelligence = 50
        
        self.setup_ui()
        self.load_pet_data()
        
        self.decay_timer = QTimer()
        self.decay_timer.timeout.connect(self.apply_stat_decay)
        self.decay_timer.start(30000)
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title_layout = QHBoxLayout()
        self.title_label = QLabel(f"🐾 My Pet: {self.pet_name}")
        self.title_label.setStyleSheet("font-size: 28px; color: white; font-weight: bold;")
        
        self.level_badge = QLabel(f"⭐ Level {self.pet_level}")
        self.level_badge.setStyleSheet("""
            QLabel {
                font-size: 16px; color: white; background-color: #6c5ce7;
                border-radius: 15px; padding: 8px 20px;
            }
        """)
        
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.level_badge)
        layout.addLayout(title_layout)
        
        # Pet display
        pet_card = QFrame()
        pet_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5268, stop:1 #424758);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        pet_layout = QVBoxLayout(pet_card)
        
        self.pet_widget = BeautifulPetWidget()
        pet_widget_container = QHBoxLayout()
        pet_widget_container.addStretch()
        pet_widget_container.addWidget(self.pet_widget)
        pet_widget_container.addStretch()
        pet_layout.addLayout(pet_widget_container)
        
        self.mood_label = QLabel(f"💝 Mood: {self.pet_mood.capitalize()}")
        self.mood_label.setStyleSheet("font-size: 20px; color: #FFD700; font-weight: bold;")
        self.mood_label.setAlignment(Qt.AlignCenter)
        pet_layout.addWidget(self.mood_label)
        
        # EXP bar
        exp_container = QWidget()
        exp_layout = QHBoxLayout(exp_container)
        exp_layout.setContentsMargins(50, 10, 50, 10)
        
        exp_label = QLabel("EXP:")
        exp_label.setStyleSheet("font-size: 14px; color: white;")
        
        self.exp_bar = QProgressBar()
        self.exp_bar.setMaximum(100)
        self.exp_bar.setValue(self.pet_exp)
        self.exp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #5c6378; border-radius: 10px;
                text-align: center; color: white; background-color: #2a2f3a;
                height: 28px; font-size: 13px; font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c5ce7, stop:1 #8b7ee8);
                border-radius: 8px;
            }
        """)
        
        exp_layout.addWidget(exp_label)
        exp_layout.addWidget(self.exp_bar, 1)
        pet_layout.addWidget(exp_container)
        
        layout.addWidget(pet_card)
        
        # Customization Section
        custom_group = QGroupBox("🎨 Customize Your Pet")
        custom_group.setStyleSheet("""
            QGroupBox {
                background-color: #424758; border: 1px solid #5c6378;
                border-radius: 15px; padding: 20px; margin-top: 10px;
                color: white; font-size: 18px; font-weight: bold;
            }
        """)
        custom_layout = QVBoxLayout(custom_group)
        
        # Pet type selector
        type_label = QLabel("Pet Type:")
        type_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        custom_layout.addWidget(type_label)
        
        type_container = QWidget()
        type_layout = QHBoxLayout(type_container)
        
        self.type_group = QButtonGroup()
        types = [("🐱 Cat", "cat"), ("🐶 Dog", "dog"), ("🐰 Bunny", "bunny")]
        for emoji, pet_type in types:
            btn = QPushButton(emoji)
            btn.setCheckable(True)
            btn.setProperty("pet_type", pet_type)
            btn.clicked.connect(lambda checked, t=pet_type: self.change_pet_type(t))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #5c6378; color: white; border: none;
                    border-radius: 10px; padding: 15px; font-size: 32px;
                }
                QPushButton:checked {
                    background-color: #6c5ce7;
                }
                QPushButton:hover {
                    background-color: #6c748c;
                }
            """)
            self.type_group.addButton(btn)
            type_layout.addWidget(btn)
            if pet_type == "cat":
                btn.setChecked(True)
        
        custom_layout.addWidget(type_container)
        
        # Color selector
        color_label = QLabel("Pet Color:")
        color_label.setStyleSheet("font-size: 14px; color: #cccccc; margin-top: 10px;")
        custom_layout.addWidget(color_label)
        
        color_container = QWidget()
        color_layout = QHBoxLayout(color_container)
        
        colors = [
            ("Gold", QColor(255, 215, 0)),
            ("Brown", QColor(139, 69, 19)),
            ("White", QColor(255, 255, 255)),
            ("Gray", QColor(128, 128, 128)),
            ("Black", QColor(50, 50, 50)),
            ("Orange", QColor(255, 140, 0))
        ]
        
        for name, color in colors:
            btn = QPushButton()
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda checked, c=color: self.change_pet_color(c))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    border: 3px solid #5c6378;
                    border-radius: 25px;
                }}
                QPushButton:hover {{
                    border: 3px solid #6c5ce7;
                }}
            """)
            color_layout.addWidget(btn)
        
        custom_layout.addWidget(color_container)
        layout.addWidget(custom_group)
        
        # Stats (rest of code same as before...)
        # Activities buttons (rest of code same as before...)
        
        scroll.setWidget(content)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def change_pet_type(self, pet_type):
        self.pet_type = pet_type
        self.pet_widget.set_pet_type(pet_type)
        print(f"Changed pet type to: {pet_type}")
    
    def change_pet_color(self, color):
        self.pet_color = color
        self.pet_widget.set_color(color)
        print(f"Changed pet color to: {color.name()}")
    
    def load_pet_data(self):
        """Load pet data"""
        try:
            result = APIClient.get_pet_data(self.user_id)
            if 'error' not in result:
                self.pet_name = result.get('pet_name', 'Buddy')
                self.pet_type = result.get('pet_type', 'cat')
                self.update_ui()
        except Exception as e:
            print(f"Failed to load pet data: {e}")
    
    def update_ui(self):
        self.title_label.setText(f"🐾 My Pet: {self.pet_name}")
        self.pet_widget.set_pet_type(self.pet_type)
        self.pet_widget.set_mood(self.pet_mood)
    
    def apply_stat_decay(self):
        pass
    
    def refresh_data(self):
        self.load_pet_data()
    
    def update_content(self, pet_name, pet_mood):
        self.pet_name = pet_name
        self.pet_mood = pet_mood
        self.update_ui()