from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                              QLineEdit, QFormLayout, QSizePolicy, QSpacerItem, 
                              QPlainTextEdit, QScrollArea, QWidget, QGroupBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

class ProfilePage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            background-color: #3a404d;
        """)
        
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        scroll_content = QWidget()
        scroll.setWidget(scroll_content)
        
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Your Profile")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Avatar Section (now square)
        avatar_frame = QFrame()
        avatar_frame.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        avatar_layout = QVBoxLayout(avatar_frame)
        avatar_layout.setAlignment(Qt.AlignCenter)
        avatar_layout.setSpacing(15)
        
        self.avatar_label = QLabel()
        # Square avatar (120x120)
        avatar_pixmap = QPixmap(":/icons/user.png").scaled(
            QSize(120, 120), 
            Qt.IgnoreAspectRatio, 
            Qt.SmoothTransformation
        )
        self.avatar_label.setPixmap(avatar_pixmap)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("background-color: #5c6378; border-radius: 5px;")
        
        change_avatar_button = QPushButton("Change Avatar")
        change_avatar_button.setIcon(QIcon(":/icons/camera.png"))
        change_avatar_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 5px;
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
        
        avatar_layout.addWidget(self.avatar_label)
        avatar_layout.addWidget(change_avatar_button)
        layout.addWidget(avatar_frame)
        
        # Personal Info Section
        personal_group = QGroupBox("Personal Information")
        personal_group.setStyleSheet("""
            QGroupBox {
                background-color: #424758;
                border: 1px solid #5c6378;
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
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
        
        form_layout = QFormLayout(personal_group)
        form_layout.setContentsMargins(10, 20, 10, 10)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(12)
        
        self.username_edit = self.create_form_field("Username:", form_layout)
        self.email_edit = self.create_form_field("Email:", form_layout)
        self.bio_edit = self.create_form_field("Bio:", form_layout, is_textarea=True)
        self.hobbies_edit = self.create_form_field("Hobbies:", form_layout)
        
        layout.addWidget(personal_group)
        
        # Password Change Section (collapsible)
        self.password_group = QGroupBox("Change Password")
        self.password_group.setCheckable(True)
        self.password_group.setChecked(False)
        self.password_group.setStyleSheet("""
            QGroupBox {
                background-color: #424758;
                border: 1px solid #5c6378;
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QGroupBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        
        password_layout = QFormLayout(self.password_group)
        password_layout.setContentsMargins(10, 20, 10, 10)
        password_layout.setHorizontalSpacing(15)
        password_layout.setVerticalSpacing(12)
        
        self.current_password = self.create_form_field("Current Password:", password_layout, is_password=True)
        self.new_password = self.create_form_field("New Password:", password_layout, is_password=True)
        self.confirm_password = self.create_form_field("Confirm Password:", password_layout, is_password=True)
        
        layout.addWidget(self.password_group)
        
        # Button Row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        save_button = QPushButton("Save Changes")
        save_button.setIcon(QIcon(":/icons/save.png"))
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setIcon(QIcon(":/icons/close.png"))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #5c6378;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #6c748c;
            }
            QPushButton:pressed {
                background-color: #4a5263;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        main_layout.addWidget(scroll)
    
    def create_form_field(self, label_text, form_layout, is_textarea=False, is_password=False):
        label = QLabel(label_text)
        label.setStyleSheet("""
            font-size: 14px; 
            color: #cccccc;
        """)
        
        if is_textarea:
            field = QPlainTextEdit()
            field.setStyleSheet("""
                QPlainTextEdit {
                    background-color: #5c6378;
                    color: white;
                    border: 1px solid #6c748c;
                    border-radius: 5px;
                    padding: 8px 12px;
                    font-size: 14px;
                    min-height: 80px;
                }
            """)
            form_layout.addRow(label, field)
        elif is_password:
            field = QLineEdit()
            field.setEchoMode(QLineEdit.Password)
            field.setStyleSheet("""
                QLineEdit {
                    background-color: #5c6378;
                    color: white;
                    border: 1px solid #6c748c;
                    border-radius: 5px;
                    padding: 8px 12px;
                    font-size: 14px;
                }
            """)
            form_layout.addRow(label, field)
        else:
            field = QLineEdit()
            field.setStyleSheet("""
                QLineEdit {
                    background-color: #5c6378;
                    color: white;
                    border: 1px solid #6c748c;
                    border-radius: 5px;
                    padding: 8px 12px;
                    font-size: 14px;
                }
            """)
            form_layout.addRow(label, field)
        
        return field
    
    def update_content(self, username):
        self.username_edit.setText(username)
        self.email_edit.setText("user@example.com")
        self.bio_edit.setPlainText("Hello! I'm using MoodMate to track and understand my emotions better.")
        self.hobbies_edit.setText("Reading, Music, Hiking, Photography")