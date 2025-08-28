from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextBrowser, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon

class HelpPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()


    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Help & Support")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)
        
        # Help Content Card
        help_card = QFrame()
        help_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        
        help_layout = QVBoxLayout(help_card)
        help_layout.setSpacing(10)
        
        # About Section
        about_title = QLabel("About MoodMate")
        about_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
            }
        """)
        
        about_text = QLabel("""
            MoodMate is your emotional companion designed to detect and respond to your feelings in real-time.
            Our app helps you understand your emotions through facial recognition, voice analysis, and text input.
        """)
        about_text.setStyleSheet("font-size: 14px; color: #cccccc;")
        about_text.setWordWrap(True)
        
        # Documentation Section
        doc_title = QLabel("Documentation")
        doc_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                padding-top: 2px;
            }
        """)
        
        doc_text = QLabel("""
            Learn how to get the most out of MoodMate with our comprehensive guides and tutorials.
        """)
        doc_text.setStyleSheet("font-size: 14px; color: #cccccc;")
        doc_text.setWordWrap(True)
        
        doc_button = QPushButton("Open Documentation")
        doc_button.setIcon(QIcon(":/icons/book.png"))
        doc_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 14px;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        # Contact Section
        contact_title = QLabel("Contact Support")
        contact_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                padding-top: 10px;
            }
        """)
        
        contact_text = QLabel("""
            Having issues or suggestions? Our support team is here to help!
            Email: support@moodmate.app
        """)
        contact_text.setStyleSheet("font-size: 14px; color: #cccccc;")
        contact_text.setWordWrap(True)
        
        contact_button = QPushButton("Contact Us")
        contact_button.setIcon(QIcon(":/icons/mail.png"))
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 4px 8px;
                font-size: 14px;
                max-width: 100px;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        # Add sections to help layout
        help_layout.addWidget(about_title)
        help_layout.addWidget(about_text)
        help_layout.addWidget(doc_title)
        help_layout.addWidget(doc_text)
        help_layout.addWidget(doc_button, 0, Qt.AlignLeft)
        help_layout.addWidget(contact_title)
        help_layout.addWidget(contact_text)
        help_layout.addWidget(contact_button, 0, Qt.AlignLeft)
        help_layout.addStretch()
        
        layout.addWidget(help_card)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))