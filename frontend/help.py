from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                              QTextBrowser, QSizePolicy, QSpacerItem, QScrollArea, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import os

class HelpPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        
        # --- MAIN LAYOUT (WITH SCROLL) ---
        # ScrollArea to make the entire page scrollable
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Content widget inside the scroll area
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15) # Spacing between sections
        
        # --- Title ---
        title = QLabel("Help & Support")
        title.setStyleSheet("font-size: 22px; color: white; font-weight: bold; margin-bottom: 5px;")
        main_layout.addWidget(title)
        
        # ==========================================================
        # 1. ABOUT SECTION (COMPACT)
        # ==========================================================
        about_card = QFrame()
        about_card.setStyleSheet("background-color: #424758; border-radius: 10px; padding: 10px;")
        about_layout = QVBoxLayout(about_card)
        about_layout.setSpacing(5)
        
        about_lbl = QLabel("About MoodMate")
        about_lbl.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        
        about_desc = QLabel("Your AI emotional companion for mental wellness.")
        about_desc.setStyleSheet("font-size: 13px; color: #cccccc;")
        about_desc.setWordWrap(True)
        
        about_layout.addWidget(about_lbl)
        about_layout.addWidget(about_desc)
        main_layout.addWidget(about_card)

        # ==========================================================
        # 2. DOCUMENTATION (README) - FIXED HEIGHT
        # ==========================================================
        doc_group_title = QLabel("📖 Documentation")
        doc_group_title.setStyleSheet("font-size: 16px; color: white; font-weight: bold; margin-top: 5px;")
        main_layout.addWidget(doc_group_title)

        # Logic to find README.md
        readme_text = "# Documentation Not Found"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(current_dir, "..", "README.md"),
            os.path.join(current_dir, "README.md")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        readme_text = f.read()
                    break 
                except: pass

        self.doc_browser = QTextBrowser()
        self.doc_browser.setMarkdown(readme_text)
        self.doc_browser.setOpenExternalLinks(True)
        
        # Fixed height
        self.doc_browser.setFixedHeight(350) 
        
        self.doc_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #5c6270;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
            }
        """)
        main_layout.addWidget(self.doc_browser)

        # ==========================================================
        # 3. CONTACT SECTION (COMPACT)
        # ==========================================================
        contact_card = QFrame()
        contact_card.setStyleSheet("background-color: #424758; border-radius: 10px; padding: 10px;")
        contact_layout = QHBoxLayout(contact_card) # Horizontal
        
        contact_info = QLabel("Need Help? Email: <b>support@moodmate.app</b>")
        contact_info.setStyleSheet("font-size: 13px; color: #cccccc;")
        contact_info.setTextFormat(Qt.RichText)
        
        contact_btn = QPushButton("Contact")
        contact_btn.setIcon(QIcon(":/icons/mail.png"))
        contact_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7; color: white; border-radius: 6px;
                padding: 6px 15px; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #7d6ee8; }
        """)
        
        contact_layout.addWidget(contact_info)
        contact_layout.addStretch()
        contact_layout.addWidget(contact_btn)
        
        main_layout.addWidget(contact_card)
        
        # Spacer
        main_layout.addStretch()

        # Final Setup
        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)