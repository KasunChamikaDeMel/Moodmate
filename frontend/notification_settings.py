"""
Notification Settings Page
Place this in: frontend/notification_settings.py
"""

from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                              QCheckBox, QSlider, QComboBox, QGroupBox,
                              QButtonGroup, QRadioButton, QMessageBox, QWidget, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
import json
import os


class NotificationSettingsPage(QFrame):
    """Complete notification customization page"""
    
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
        
        # Title
        title = QLabel("🔔 Notification Settings")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                color: white;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Pet Selection
        pet_group = self.create_group("🐾 Choose Your Companion")
        pet_layout = pet_group.layout()
        
        pet_desc = QLabel("Select which pet appears in notifications:")
        pet_desc.setStyleSheet("font-size: 14px; color: #cccccc; padding-bottom: 10px;")
        pet_layout.addWidget(pet_desc)
        
        pet_container = QWidget()
        pet_container.setStyleSheet("""
            QWidget {
                background-color: #5c6378;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        pet_btn_layout = QHBoxLayout(pet_container)
        pet_btn_layout.setSpacing(15)
        
        self.pet_group = QButtonGroup()
        
        pets = [
            ("🐱 Cat", "cat", "Playful and independent"),
            ("🐶 Dog", "dog", "Loyal and energetic"),
            ("🐰 Bunny", "bunny", "Gentle and calm")
        ]
        
        for emoji_name, pet_type, desc in pets:
            # Create pet button - returns tuple (container, radio_button)
            container, radio_btn = self.create_pet_button(emoji_name, pet_type, desc)
            self.pet_group.addButton(radio_btn)  # Add the radio button, not container
            pet_btn_layout.addWidget(container)  # Add container to layout
        
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
                border: 1px solid #6c748c;
                height: 8px;
                background: #424758;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #6c5ce7;
                border: 2px solid #5865f2;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        
        self.duration_value = QLabel("20s")
        self.duration_value.setStyleSheet("font-size: 14px; color: white; min-width: 40px;")
        self.duration_slider.valueChanged.connect(
            lambda v: self.duration_value.setText(f"{v}s")
        )
        
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_slider, 1)
        duration_layout.addWidget(self.duration_value)
        
        behavior_layout.addWidget(duration_container)
        
        # Position
        position_container = QWidget()
        position_layout = QHBoxLayout(position_container)
        
        position_label = QLabel("Position:")
        position_label.setStyleSheet("font-size: 14px; color: #cccccc; min-width: 130px;")
        
        self.position_combo = QComboBox()
        self.position_combo.addItems([
            "Bottom Right",
            "Bottom Left",
            "Top Right",
            "Top Left"
        ])
        self.position_combo.setStyleSheet("""
            QComboBox {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QComboBox:hover { border: 2px solid #6c5ce7; }
            QComboBox QAbstractItemView {
                background-color: #424758;
                color: white;
                selection-background-color: #6c5ce7;
            }
        """)
        
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_combo, 1)
        
        behavior_layout.addWidget(position_container)
        layout.addWidget(behavior_group)
        
        # Sound Settings
        sound_group = self.create_group("🔊 Sound Settings")
        sound_layout = sound_group.layout()
        
        self.enable_sound = QCheckBox("Play notification sound")
        self.enable_sound.setChecked(True)
        self.enable_sound.setStyleSheet(self.checkbox_style())
        sound_layout.addWidget(self.enable_sound)
        
        layout.addWidget(sound_group)
        
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
                background-color: #5c6378;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #6c748c; }
        """)
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 32px;
                font-size: 15px;
                font-weight: bold;
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
                background-color: #424758;
                border: 1px solid #5c6378;
                border-radius: 12px;
                padding: 20px;
                margin-top: 10px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                border: none;
                padding: 0;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        return group
    
    def create_pet_button(self, text, pet_type, description):
        """Create pet selection button - returns (container, radio_button) tuple"""
        btn = QRadioButton()
        btn.setProperty("pet_type", pet_type)
        
        if pet_type == "cat":
            btn.setChecked(True)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        
        emoji_label = QLabel(text)
        emoji_label.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        emoji_label.setAlignment(Qt.AlignCenter)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 12px; color: #b5b8bd;")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        container_layout.addWidget(btn, alignment=Qt.AlignCenter)
        container_layout.addWidget(emoji_label)
        container_layout.addWidget(desc_label)
        
        btn.setStyleSheet("""
            QRadioButton {
                spacing: 0px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #6c748c;
                background-color: #424758;
            }
            QRadioButton::indicator:checked {
                background-color: #6c5ce7;
                border-color: #6c5ce7;
            }
        """)
        
        # Return both container and radio button
        return container, btn
    
    def checkbox_style(self):
        return """
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 10px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #6c748c;
                background-color: #5c6378;
            }
            QCheckBox::indicator:checked {
                background-color: #6c5ce7;
                border-color: #6c5ce7;
            }
        """
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                self.enable_notifications.setChecked(settings.get('enabled', True))
                self.duration_slider.setValue(settings.get('duration', 20))
                self.position_combo.setCurrentText(settings.get('position', 'Bottom Right'))
                self.enable_sound.setChecked(settings.get('sound_enabled', True))
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
                'position': self.position_combo.currentText(),
                'sound_enabled': self.enable_sound.isChecked(),
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
                "Notification settings saved successfully!\n\n"
                f"Pet: {pet_type.capitalize()}\n"
                f"Duration: {settings['duration']}s\n"
                f"Position: {settings['position']}")
                
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
                "Preview notification shown!")
        else:
            QMessageBox.warning(self, "Preview", "Preview not available.")