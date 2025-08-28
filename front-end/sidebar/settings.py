from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, 
                              QHBoxLayout, QLineEdit, QComboBox, QCheckBox,
                              QSizePolicy, QScrollArea, QWidget, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class SettingsPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            background-color: #3a404d;
        """)
        
        # Create scroll area for settings
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background: #424758;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #6c5ce7;
                min-height: 30px;
                border-radius: 4px;
            }
        """)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                color: white;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Pet Settings Section
        pet_group = self.create_settings_group("Pet Settings", ":/icons/pet.png")
        pet_layout = pet_group.layout()
        
        pet_name_label = QLabel("Pet Name:")
        pet_name_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        self.pet_name_edit = QLineEdit()
        self.pet_name_edit.setPlaceholderText("Enter your pet's name")
        self.pet_name_edit.setStyleSheet("""
            QLineEdit {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
        """)
        
        pet_layout.addWidget(pet_name_label)
        pet_layout.addWidget(self.pet_name_edit)
        layout.addWidget(pet_group)
        
        # Appearance Settings Section
        appearance_group = self.create_settings_group("Appearance", ":/icons/paint.png")
        appearance_layout = appearance_group.layout()
        
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Blue", "Purple", "System"])
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
        """)
        
        appearance_layout.addWidget(theme_label)
        appearance_layout.addWidget(self.theme_combo)
        layout.addWidget(appearance_group)
        
        # Device Permissions Section
        permissions_group = self.create_settings_group("Device Permissions", ":/icons/permissions.png")
        permissions_layout = permissions_group.layout()
        
        # Microphone Permission
        mic_layout = QHBoxLayout()
        mic_label = QLabel("Microphone Access:")
        mic_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        self.mic_combo = QComboBox()
        self.mic_combo.addItems(["Allow", "Ask Every Time", "Deny"])
        self.mic_combo.setStyleSheet("""
            QComboBox {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 150px;
            }
        """)
        
        mic_layout.addWidget(mic_label)
        mic_layout.addWidget(self.mic_combo)
        mic_layout.addStretch()
        permissions_layout.addLayout(mic_layout)
        
        # Camera Permission
        cam_layout = QHBoxLayout()
        cam_label = QLabel("Camera Access:")
        cam_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        self.cam_combo = QComboBox()
        self.cam_combo.addItems(["Allow", "Ask Every Time", "Deny"])
        self.cam_combo.setStyleSheet("""
            QComboBox {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 150px;
            }
        """)
        
        cam_layout.addWidget(cam_label)
        cam_layout.addWidget(self.cam_combo)
        cam_layout.addStretch()
        permissions_layout.addLayout(cam_layout)
        
        layout.addWidget(permissions_group)
        
        # Notifications Settings Section
        notif_group = self.create_settings_group("Notifications", ":/icons/bell.png")
        notif_layout = notif_group.layout()
        
        self.notif_check = QCheckBox("Enable notifications")
        self.notif_check.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        
        self.sound_check = QCheckBox("Enable notification sounds")
        self.sound_check.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
        """)
        
        notif_layout.addWidget(self.notif_check)
        notif_layout.addWidget(self.sound_check)
        layout.addWidget(notif_group)
        
        # Save Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_button = QPushButton("Save Settings")
        save_button.setIcon(QIcon(":/icons/save.png"))
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def create_settings_group(self, title, icon_path):
        group = QGroupBox()
        group.setStyleSheet("""
            QGroupBox {
                background-color: #424758;
                border: 1px solid #5c6378;
                border-radius: 12px;
                padding: 15px;
                margin-top: 5px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        # Custom title with icon
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 5)
        
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(20, 20))
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        return group
    
    def update_content(self, pet_name):
        self.pet_name_edit.setText(pet_name)