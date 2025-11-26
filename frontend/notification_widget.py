"""
Windows Toast Notification with Animated Pet
All animations drawn programmatically - no external assets required
Includes NotificationSettingsPage
"""

from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QGraphicsDropShadowEffect, QApplication,
                              QFrame, QCheckBox, QSlider, QComboBox, QSpinBox, QGroupBox,
                              QButtonGroup, QRadioButton, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, Signal, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush, QRadialGradient, QPainterPath, QIcon
import random
import math
import json
import os


class AnimatedPetWidget(QWidget):
    """Self-contained animated pet - no external files needed"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        self.pet_type = "cat"
        self.pet_mood = "neutral"
        self.animation_frame = 0
        self.time_offset = 0
        self.blink_timer = 0
        self.is_blinking = False
        self.body_bounce = 0
        self.ear_wiggle = 0
        self.tail_swing = 0
        self.particles = []
        
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(50)
    
    def set_pet_type(self, pet_type):
        self.pet_type = pet_type.lower()
        self.update()
    
    def set_mood(self, mood):
        self.pet_mood = mood.lower()
        self.particles = []
        self.update()
    
    def update_animation(self):
        self.time_offset += 0.1
        self.animation_frame = (self.animation_frame + 1) % 1000
        
        # Breathing
        self.body_bounce = math.sin(self.time_offset * 2) * 3
        
        # Blinking
        self.blink_timer += 1
        if self.blink_timer > 60:
            self.is_blinking = True
            if self.blink_timer > 65:
                self.is_blinking = False
                self.blink_timer = random.randint(-30, 0)
        
        # Mood effects
        if self.pet_mood == "happy" and random.random() < 0.1:
            self.particles.append({
                'x': random.randint(-30, 30),
                'y': random.randint(-30, 30),
                'life': 30,
                'size': random.randint(2, 5)
            })
        
        # Update particles
        self.particles = [p for p in self.particles if p['life'] > 0]
        for p in self.particles:
            p['life'] -= 1
            p['y'] -= 1
        
        self.ear_wiggle = math.sin(self.time_offset * 1.5) * 5
        self.tail_swing = math.sin(self.time_offset * 2) * 15
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx = self.width() / 2
        cy = self.height() / 2 + self.body_bounce
        
        if self.pet_type == "cat":
            self.draw_cat(painter, cx, cy)
        elif self.pet_type == "dog":
            self.draw_dog(painter, cx, cy)
        elif self.pet_type == "bunny":
            self.draw_bunny(painter, cx, cy)
        
        # Draw particles
        for p in self.particles:
            alpha = int((p['life'] / 30) * 255)
            painter.setBrush(QColor(255, 255, 0, alpha))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(cx + p['x'], cy + p['y']), p['size'], p['size'])
    
    def get_mood_colors(self):
        colors = {
            "happy": {"body": QColor(255, 215, 0), "accent": QColor(255, 165, 0)},
            "sad": {"body": QColor(135, 206, 235), "accent": QColor(70, 130, 180)},
            "angry": {"body": QColor(255, 99, 71), "accent": QColor(220, 20, 60)},
            "stress": {"body": QColor(255, 140, 0), "accent": QColor(255, 69, 0)},
            "sleepy": {"body": QColor(147, 112, 219), "accent": QColor(138, 43, 226)},
            "sleep": {"body": QColor(147, 112, 219), "accent": QColor(138, 43, 226)},
            "neutral": {"body": QColor(152, 251, 152), "accent": QColor(60, 179, 113)}
        }
        return colors.get(self.pet_mood, colors["neutral"])
    
    def draw_cat(self, painter, cx, cy):
        colors = self.get_mood_colors()
        
        # Shadow
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 50))
        painter.drawEllipse(QPointF(cx, cy + 45), 35, 8)
        
        # Body
        gradient = QRadialGradient(cx, cy - 5, 35)
        gradient.setColorAt(0, colors["body"].lighter(110))
        gradient.setColorAt(1, colors["body"])
        painter.setBrush(gradient)
        painter.setPen(QPen(colors["accent"], 2))
        painter.drawEllipse(QPointF(cx, cy), 35, 40)
        
        # Ears
        painter.setBrush(colors["accent"])
        left_ear = [
            QPointF(cx - 20, cy - 35),
            QPointF(cx - 25 + self.ear_wiggle, cy - 50),
            QPointF(cx - 15, cy - 40)
        ]
        painter.drawPolygon(left_ear)
        
        right_ear = [
            QPointF(cx + 20, cy - 35),
            QPointF(cx + 25 - self.ear_wiggle, cy - 50),
            QPointF(cx + 15, cy - 40)
        ]
        painter.drawPolygon(right_ear)
        
        # Eyes
        eye_y = cy - 15
        if self.is_blinking or self.pet_mood in ["sleep", "sleepy"]:
            painter.setPen(QPen(Qt.black, 3))
            painter.drawLine(int(cx - 18), int(eye_y), int(cx - 12), int(eye_y))
            painter.drawLine(int(cx + 12), int(eye_y), int(cx + 18), int(eye_y))
        else:
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPointF(cx - 15, eye_y), 8, 10)
            painter.drawEllipse(QPointF(cx + 15, eye_y), 8, 10)
            
            painter.setBrush(Qt.black)
            painter.drawEllipse(QPointF(cx - 15, eye_y + 2), 4, 6)
            painter.drawEllipse(QPointF(cx + 15, eye_y + 2), 4, 6)
            
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPointF(cx - 13, eye_y - 1), 2, 2)
            painter.drawEllipse(QPointF(cx + 17, eye_y - 1), 2, 2)
        
        # Nose
        painter.setBrush(QColor(255, 105, 180))
        painter.drawEllipse(QPointF(cx, cy - 5), 4, 3)
        
        # Mouth
        painter.setPen(QPen(Qt.black, 2))
        if self.pet_mood == "happy":
            path = QPainterPath()
            path.moveTo(cx - 12, cy)
            path.quadTo(cx, cy + 8, cx + 12, cy)
            painter.drawPath(path)
        elif self.pet_mood == "angry":
            path = QPainterPath()
            path.moveTo(cx - 12, cy + 5)
            path.quadTo(cx, cy - 3, cx + 12, cy + 5)
            painter.drawPath(path)
        
        # Whiskers
        painter.drawLine(int(cx - 25), int(cy - 5), int(cx - 38), int(cy - 8))
        painter.drawLine(int(cx - 25), int(cy), int(cx - 38), int(cy + 2))
        painter.drawLine(int(cx + 25), int(cy - 5), int(cx + 38), int(cy - 8))
        painter.drawLine(int(cx + 25), int(cy), int(cx + 38), int(cy + 2))
    
    def draw_dog(self, painter, cx, cy):
        colors = self.get_mood_colors()
        
        gradient = QRadialGradient(cx, cy, 35)
        gradient.setColorAt(0, colors["body"].lighter(110))
        gradient.setColorAt(1, colors["body"])
        painter.setBrush(gradient)
        painter.setPen(QPen(colors["accent"], 2))
        painter.drawEllipse(QPointF(cx, cy), 35, 40)
        
        painter.setBrush(colors["accent"])
        painter.drawEllipse(QPointF(cx - 35, cy - 10), 12, 25)
        painter.drawEllipse(QPointF(cx + 35, cy - 10), 12, 25)
        
        painter.setBrush(colors["body"].lighter(115))
        painter.drawEllipse(QPointF(cx, cy + 5), 18, 15)
        
        eye_y = cy - 15
        if self.is_blinking:
            painter.setPen(QPen(Qt.black, 3))
            painter.drawLine(int(cx - 18), int(eye_y), int(cx - 12), int(eye_y))
            painter.drawLine(int(cx + 12), int(eye_y), int(cx + 18), int(eye_y))
        else:
            painter.setBrush(Qt.white)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(cx - 15, eye_y), 8, 10)
            painter.drawEllipse(QPointF(cx + 15, eye_y), 8, 10)
            painter.setBrush(Qt.black)
            painter.drawEllipse(QPointF(cx - 15, eye_y + 2), 4, 6)
            painter.drawEllipse(QPointF(cx + 15, eye_y + 2), 4, 6)
        
        painter.setBrush(Qt.black)
        painter.drawEllipse(QPointF(cx, cy + 10), 5, 4)
    
    def draw_bunny(self, painter, cx, cy):
        colors = self.get_mood_colors()
        
        gradient = QRadialGradient(cx, cy, 35)
        gradient.setColorAt(0, colors["body"].lighter(110))
        gradient.setColorAt(1, colors["body"])
        painter.setBrush(gradient)
        painter.setPen(QPen(colors["accent"], 2))
        painter.drawEllipse(QPointF(cx, cy), 35, 38)
        
        painter.setBrush(colors["accent"])
        painter.drawEllipse(QPointF(cx - 18, cy - 50), 10, 35)
        painter.drawEllipse(QPointF(cx + 18, cy - 50), 10, 35)
        
        painter.setBrush(QColor(255, 182, 193))
        painter.drawEllipse(QPointF(cx - 18, cy - 45), 5, 20)
        painter.drawEllipse(QPointF(cx + 18, cy - 45), 5, 20)
        
        eye_y = cy - 15
        if self.is_blinking:
            painter.setPen(QPen(Qt.black, 3))
            painter.drawLine(int(cx - 18), int(eye_y), int(cx - 12), int(eye_y))
            painter.drawLine(int(cx + 12), int(eye_y), int(cx + 18), int(eye_y))
        else:
            painter.setBrush(Qt.white)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(cx - 15, eye_y), 8, 10)
            painter.drawEllipse(QPointF(cx + 15, eye_y), 8, 10)
            painter.setBrush(Qt.black)
            painter.drawEllipse(QPointF(cx - 15, eye_y + 2), 4, 6)
            painter.drawEllipse(QPointF(cx + 15, eye_y + 2), 4, 6)
        
        painter.setBrush(QColor(255, 105, 180))
        painter.drawEllipse(QPointF(cx, cy - 5), 4, 3)


class WindowsToastNotification(QWidget):
    """Windows toast notification with animated pet"""
    
    closed = Signal()
    action_clicked = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(420, 280)
        
        self.current_emotion = None
        self.pet_type = "cat"
        self.setup_ui()
        self.setup_animations()
        self.setup_shadow()
        
        self.dismiss_timer = QTimer()
        self.dismiss_timer.setSingleShot(True)  # Only fire once
        self.dismiss_timer.timeout.connect(self.hide_notification)
    
    def setup_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
    
    def setup_ui(self):
        container = QWidget(self)
        container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2d31, stop:1 #1e1f22);
                border-radius: 12px;
                border: 2px solid #3a3d42;
            }
        """)
        container.setGeometry(5, 5, 410, 270)
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(18, 15, 18, 15)
        main_layout.setSpacing(12)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        icon_label = QLabel("🔔")
        icon_label.setStyleSheet("font-size: 20px;")
        
        app_name = QLabel("MoodMate Companion")
        app_name.setStyleSheet("QLabel { font-size: 15px; font-weight: bold; color: #ffffff; }")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(app_name)
        header_layout.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: #b5b8bd;
                border: none; font-size: 24px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #e74c3c; color: white; }
        """)
        close_btn.clicked.connect(self.hide_notification)
        header_layout.addWidget(close_btn)
        
        main_layout.addLayout(header_layout)
        
        # Content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        self.pet_widget = AnimatedPetWidget()
        content_layout.addWidget(self.pet_widget)
        
        message_layout = QVBoxLayout()
        message_layout.setSpacing(8)
        
        self.emotion_label = QLabel()
        self.emotion_label.setStyleSheet("QLabel { font-size: 18px; font-weight: bold; color: #ffffff; }")
        
        self.pet_message = QLabel()
        self.pet_message.setWordWrap(True)
        self.pet_message.setStyleSheet("QLabel { font-size: 13px; color: #e3e5e8; font-style: italic; }")
        
        tips_container = QWidget()
        tips_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e1f22, stop:1 #2b2d31);
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #3a3d42;
            }
        """)
        tips_layout = QVBoxLayout(tips_container)
        tips_layout.setContentsMargins(10, 8, 10, 8)
        tips_layout.setSpacing(5)
        
        tips_title = QLabel("💡 Quick Relief Tips:")
        tips_title.setStyleSheet("QLabel { font-size: 12px; color: #b5b8bd; font-weight: bold; }")
        
        self.tips_label = QLabel()
        self.tips_label.setWordWrap(True)
        self.tips_label.setStyleSheet("QLabel { font-size: 12px; color: #e3e5e8; line-height: 1.5; }")
        
        tips_layout.addWidget(tips_title)
        tips_layout.addWidget(self.tips_label)
        
        message_layout.addWidget(self.emotion_label)
        message_layout.addWidget(self.pet_message)
        message_layout.addWidget(tips_container)
        message_layout.addStretch()
        
        content_layout.addLayout(message_layout, 1)
        main_layout.addLayout(content_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.better_btn = QPushButton("✓ I'm Feeling Better")
        self.better_btn.setStyleSheet("""
            QPushButton {
                background-color: #248046; color: white; border: none;
                border-radius: 6px; padding: 10px 15px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2d9d5a; }
        """)
        self.better_btn.clicked.connect(lambda: self.handle_action("better"))
        
        self.help_btn = QPushButton("📚 Get More Help")
        self.help_btn.setStyleSheet("""
            QPushButton {
                background-color: #4752c4; color: white; border: none;
                border-radius: 6px; padding: 10px 15px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5865f2; }
        """)
        self.help_btn.clicked.connect(lambda: self.handle_action("help"))
        
        button_layout.addWidget(self.better_btn)
        button_layout.addWidget(self.help_btn)
        
        main_layout.addLayout(button_layout)
    
    def setup_animations(self):
        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setEasingCurve(QEasingCurve.OutBack)
        self.slide_animation.setDuration(600)
    
    def set_pet_type(self, pet_type):
        self.pet_type = pet_type
        self.pet_widget.set_pet_type(pet_type)
    
    def show_notification(self, emotion, source="face", duration=None):
        # Stop any existing timer first
        self.dismiss_timer.stop()
        
        self.current_emotion = emotion.lower()
        
        # Get duration from settings if not provided (default 20 seconds)
        if duration is None:
            duration = 20000  # Default 20 seconds in milliseconds
        else:
            duration = duration * 1000  # Convert seconds to milliseconds
        
        emotion_data = {
            "stress": {
                "icon": "😰", "title": "Stress Detected", "color": "#FF8C00",
                "pet_says": [
                    "Hey there! I can see you're stressed. Let's take a moment together!",
                    "Whoa, buddy! Take it easy. I'm here to help you calm down!",
                    "You seem tense! How about we do some relaxing together?"
                ],
                "tips": [
                    "• Close your eyes and take 5 slow, deep breaths\n• Count to 4 while inhaling, hold for 4, exhale for 4\n• Try the 5-4-3-2-1 grounding technique",
                    "• Step away from your work for 5 minutes\n• Do some gentle stretching exercises\n• Listen to calming nature sounds",
                    "• Write down what's bothering you\n• Talk to a friend or family member\n• Take a short walk outside"
                ]
            },
            "angry": {
                "icon": "😠", "title": "Anger Detected", "color": "#FF6347",
                "pet_says": [
                    "Whoa! I can feel that anger. Let's cool down together, okay?",
                    "Hey! Before you explode, let me help you feel better!",
                    "I see you're upset. Want to talk about it with me?"
                ],
                "tips": [
                    "• Count slowly to 10 before reacting\n• Take 3 deep breaths to calm down\n• Step away from the situation temporarily",
                    "• Express your feelings by writing them down\n• Do 10 jumping jacks to release energy\n• Punch a pillow (not people!)",
                    "• Talk to someone you trust\n• Go for a brisk walk outside\n• Listen to your favorite calming music"
                ]
            },
            "sleepy": {
                "icon": "😴", "title": "Sleepiness Detected", "color": "#9370DB",
                "pet_says": [
                    "Yawn~ You look tired! Maybe we both need a power nap?",
                    "Feeling sleepy? Let's energize together or take a rest!",
                    "Zzz... Oh wait, you're the one who's sleepy! Let me help!"
                ],
                "tips": [
                    "• Take a 15-20 minute power nap\n• Avoid sleeping longer than 30 minutes\n• Set an alarm to wake up refreshed",
                    "• Splash cold water on your face\n• Do 10 quick jumping jacks\n• Open windows for fresh air",
                    "• Drink a glass of cold water\n• Stand up and stretch for 2 minutes\n• Take a short walk outside"
                ]
            },
            "sleep": {
                "icon": "😴", "title": "Sleepiness Detected", "color": "#9370DB",
                "pet_says": [
                    "Yawn~ You look tired! Maybe we both need a power nap?",
                    "Feeling sleepy? Let's energize together or take a rest!",
                    "Zzz... Oh wait, you're the one who's sleepy! Let me help!"
                ],
                "tips": [
                    "• Take a 15-20 minute power nap\n• Avoid sleeping longer than 30 minutes\n• Set an alarm to wake up refreshed",
                    "• Splash cold water on your face\n• Do 10 quick jumping jacks\n• Open windows for fresh air",
                    "• Drink a glass of cold water\n• Stand up and stretch for 2 minutes\n• Take a short walk outside"
                ]
            }
        }
        
        data = emotion_data.get(self.current_emotion, emotion_data["stress"])
        
        self.emotion_label.setText(f"{data['icon']} {data['title']}")
        self.emotion_label.setStyleSheet(f"QLabel {{ font-size: 18px; font-weight: bold; color: {data['color']}; }}")
        self.pet_message.setText(random.choice(data["pet_says"]))
        self.tips_label.setText(random.choice(data["tips"]))
        self.pet_widget.set_mood(self.current_emotion)
        
        screen = QApplication.primaryScreen().geometry()
        end_x = screen.width() - self.width() - 20
        end_y = screen.height() - self.height() - 70
        start_y = screen.height()
        
        self.slide_animation.setStartValue(QPoint(end_x, start_y))
        self.slide_animation.setEndValue(QPoint(end_x, end_y))
        
        self.show()
        # ========================================
        try:
            self.slide_animation.finished.disconnect()
        except:
            pass
        # =======================================
        
        
        self.slide_animation.start()
        # Start timer with the specified duration (ensure it's stopped first)
        self.dismiss_timer.stop()
        self.dismiss_timer.start(int(duration))
    
    def hide_notification(self):
        self.dismiss_timer.stop()
        screen = QApplication.primaryScreen().geometry()
        start_pos = self.pos()
        end_y = screen.height()
        
        self.slide_animation.setStartValue(start_pos)
        self.slide_animation.setEndValue(QPoint(start_pos.x(), end_y))
        # ========================================
        try:
            self.slide_animation.finished.disconnect()
        except:
            pass
            
        # self.slide_animation.finished.connect(self.hide)
        # ========================================
        self.slide_animation.finished.connect(self.hide)
        self.slide_animation.start()
        self.closed.emit()
    
    def handle_action(self, action):
        self.action_clicked.emit(action)
        self.hide_notification()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()


class NotificationSettingsPage(QFrame):
    """Notification customization page"""
    
    settings_changed = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.settings_file = "notification_settings.json"
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("🔔 Notification Settings")
        title.setStyleSheet("font-size: 28px; color: white; font-weight: bold; padding-bottom: 10px;")
        layout.addWidget(title)
        
        # Pet Selection
        pet_group = self.create_group("🐾 Choose Your Companion")
        pet_layout = pet_group.layout()
        
        pet_desc = QLabel("Select which pet appears in notifications:")
        pet_desc.setStyleSheet("font-size: 14px; color: #cccccc; padding-bottom: 10px;")
        pet_layout.addWidget(pet_desc)
        
        pet_container = QWidget()
        pet_container.setStyleSheet("QWidget { background-color: #5c6378; border-radius: 10px; padding: 15px; }")
        pet_btn_layout = QHBoxLayout(pet_container)
        pet_btn_layout.setSpacing(15)
        
        self.pet_group = QButtonGroup()
        
        pets = [("🐱 Cat", "cat"), ("🐶 Dog", "dog"), ("🐰 Bunny", "bunny")]
        
        for emoji_name, pet_type in pets:
            btn = QRadioButton(emoji_name)
            btn.setProperty("pet_type", pet_type)
            if pet_type == "cat":
                btn.setChecked(True)
            btn.setStyleSheet("""
                QRadioButton {
                    color: white; font-size: 16px; spacing: 8px; padding: 8px;
                }
                QRadioButton::indicator {
                    width: 20px; height: 20px; border-radius: 10px;
                    border: 2px solid #6c748c; background-color: #424758;
                }
                QRadioButton::indicator:checked {
                    background-color: #6c5ce7; border-color: #6c5ce7;
                }
            """)
            self.pet_group.addButton(btn)
            pet_btn_layout.addWidget(btn)
        
        pet_layout.addWidget(pet_container)
        layout.addWidget(pet_group)
        
        # Notification Behavior
        behavior_group = self.create_group("⚙️ Notification Behavior")
        behavior_layout = behavior_group.layout()
        
        self.enable_notifications = QCheckBox("Enable emotion notifications")
        self.enable_notifications.setChecked(True)
        self.enable_notifications.setStyleSheet(self.checkbox_style())
        behavior_layout.addWidget(self.enable_notifications)
        
        # Duration
        duration_container = QWidget()
        duration_layout = QHBoxLayout(duration_container)
        duration_layout.setContentsMargins(0, 10, 0, 10)
        
        duration_label = QLabel("Display Duration:")
        duration_label.setStyleSheet("font-size: 14px; color: #cccccc; min-width: 130px;")
        
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setMinimum(5)
        self.duration_slider.setMaximum(30)
        self.duration_slider.setValue(20)
        self.duration_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #6c748c; height: 8px;
                background: #424758; border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #6c5ce7; border: 2px solid #5865f2;
                width: 18px; margin: -5px 0; border-radius: 9px;
            }
        """)
        
        self.duration_value = QLabel("20s")
        self.duration_value.setStyleSheet("font-size: 14px; color: white; min-width: 40px;")
        self.duration_slider.valueChanged.connect(lambda v: self.duration_value.setText(f"{v}s"))
        
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_slider, 1)
        duration_layout.addWidget(self.duration_value)
        
        behavior_layout.addWidget(duration_container)
        layout.addWidget(behavior_group)
        
        # Trigger Emotions
        trigger_group = self.create_group("🎯 Trigger Emotions")
        trigger_layout = trigger_group.layout()
        
        trigger_desc = QLabel("Show notifications when these emotions are detected:")
        trigger_desc.setStyleSheet("font-size: 14px; color: #cccccc; padding-bottom: 10px;")
        trigger_layout.addWidget(trigger_desc)
        
        self.stress_trigger = QCheckBox("😰 Stress")
        self.stress_trigger.setChecked(True)
        self.stress_trigger.setStyleSheet(self.checkbox_style())
        
        self.angry_trigger = QCheckBox("😠 Anger")
        self.angry_trigger.setChecked(True)
        self.angry_trigger.setStyleSheet(self.checkbox_style())
        
        self.sleepy_trigger = QCheckBox("😴 Sleepiness")
        self.sleepy_trigger.setChecked(True)
        self.sleepy_trigger.setStyleSheet(self.checkbox_style())
        
        trigger_layout.addWidget(self.stress_trigger)
        trigger_layout.addWidget(self.angry_trigger)
        trigger_layout.addWidget(self.sleepy_trigger)
        
        layout.addWidget(trigger_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        preview_btn = QPushButton("👁️ Preview Notification")
        preview_btn.clicked.connect(self.preview_notification)
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #5c6378; color: white; border: none;
                border-radius: 8px; padding: 12px 24px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #6c748c; }
        """)
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7; color: white; border: none;
                border-radius: 8px; padding: 12px 32px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background-color: #7d6ee8; }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(preview_btn)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def create_group(self, title):
        group = QGroupBox()
        group.setStyleSheet("""
            QGroupBox {
                background-color: #424758; border: 1px solid #5c6378;
                border-radius: 12px; padding: 20px; margin-top: 10px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px; color: white; font-weight: bold;
                border: none; padding: 0; margin-bottom: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        return group
    
    def checkbox_style(self):
        return """
            QCheckBox {
                color: white; font-size: 14px; spacing: 10px; padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px; height: 20px; border-radius: 4px;
                border: 2px solid #6c748c; background-color: #5c6378;
            }
            QCheckBox::indicator:checked {
                background-color: #6c5ce7; border-color: #6c5ce7;
            }
        """
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                self.enable_notifications.setChecked(settings.get('enabled', True))
                self.duration_slider.setValue(settings.get('duration', 20))
                self.stress_trigger.setChecked(settings.get('trigger_stress', True))
                self.angry_trigger.setChecked(settings.get('trigger_angry', True))
                self.sleepy_trigger.setChecked(settings.get('trigger_sleepy', True))
                
                pet_type = settings.get('pet_type', 'cat')
                for btn in self.pet_group.buttons():
                    if btn.property("pet_type") == pet_type:
                        btn.setChecked(True)
                
                print("✅ Notification settings loaded")
            except Exception as e:
                print(f"Error loading notification settings: {e}")
    
    def save_settings(self):
        try:
            pet_type = "cat"
            for btn in self.pet_group.buttons():
                if btn.isChecked():
                    pet_type = btn.property("pet_type")
                    break
            
            settings = {
                'enabled': self.enable_notifications.isChecked(),
                'pet_type': pet_type,
                'duration': self.duration_slider.value(),
                'trigger_stress': self.stress_trigger.isChecked(),
                'trigger_angry': self.angry_trigger.isChecked(),
                'trigger_sleepy': self.sleepy_trigger.isChecked()
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            if self.parent_window:
                if hasattr(self.parent_window, 'notification_window'):
                    self.parent_window.notification_window.set_pet_type(pet_type)
                    
                if hasattr(self.parent_window, 'notifications_enabled'):
                    self.parent_window.notifications_enabled = settings['enabled']
            
            self.settings_changed.emit(settings)
            
            QMessageBox.information(self, "Success", 
                f"Notification settings saved!\n\nPet: {pet_type.capitalize()}\nDuration: {settings['duration']}s")
                
            print(f"✅ Notification settings saved: {pet_type}, {settings['duration']}s")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings:\n{str(e)}")
    
    def preview_notification(self):
        if self.parent_window and hasattr(self.parent_window, 'notification_window'):
            for btn in self.pet_group.buttons():
                if btn.isChecked():
                    pet_type = btn.property("pet_type")
                    self.parent_window.notification_window.set_pet_type(pet_type)
                    break
            
            self.parent_window.notification_window.show_notification("stress", "preview")
            QMessageBox.information(self, "Preview", 
                "Preview notification shown!\n\nThis is how it will appear when emotions are detected.")
        else:
            QMessageBox.warning(self, "Preview", "Preview not available.")