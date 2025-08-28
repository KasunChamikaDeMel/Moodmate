from PySide6.QtWidgets import (QFrame, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QComboBox, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class HistoryPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        # Title and controls
        title_layout = QHBoxLayout()
        
        title = QLabel("Mood History")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                font-weight: bold;
            }
        """)
        
        self.time_filter = QComboBox()
        self.time_filter.addItems(["Last 24 hours", "Last week", "Last month", "All time"])
        self.time_filter.setStyleSheet("""
            QComboBox {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                min-width: 50px;
            }
        """)
        
        export_button = QPushButton("Export Data")
        export_button.setIcon(QIcon(":/icons/export.png"))
        export_button.setStyleSheet("""
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
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(self.time_filter)
        title_layout.addWidget(export_button)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #424758;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
                border: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #5c6378;
            }
            QListWidget::item:selected {
                background-color: #6c5ce7;
            }
        """)
        
        # Stats card
        stats_card = QFrame()
        stats_card.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 15px;
                padding: 5px;
            }
        """)
        
        stats_layout = QVBoxLayout(stats_card)
        
        stats_title = QLabel("Mood Statistics")
        stats_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                padding-bottom: 5px;
            }
        """)
        
        self.happy_stat = QLabel("Happy: 0%")
        self.sad_stat = QLabel("Sad: 0%")
        self.angry_stat = QLabel("Angry: 0%")
        self.neutral_stat = QLabel("Neutral: 0%")
        
        for label in [self.happy_stat, self.sad_stat, self.angry_stat, self.neutral_stat]:
            label.setStyleSheet("font-size: 16px; color: #cccccc;")
        
        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(self.happy_stat)
        stats_layout.addWidget(self.sad_stat)
        stats_layout.addWidget(self.angry_stat)
        stats_layout.addWidget(self.neutral_stat)
        
        layout.addLayout(title_layout)
        layout.addWidget(self.history_list, 1)
        layout.addWidget(stats_card)
    
    def update_content(self, history):
        self.history_list.clear()
        
        for mood, timestamp in history[-50:]:  # Show last 50 entries
            item = QListWidgetItem(f"{timestamp}: {mood.capitalize()}")
            self.history_list.addItem(item)
        
        # Calculate stats
        total = len(history)
        if total > 0:
            happy = sum(1 for m, _ in history if m == "happy") / total * 100
            sad = sum(1 for m, _ in history if m == "sad") / total * 100
            angry = sum(1 for m, _ in history if m == "angry") / total * 100
            neutral = sum(1 for m, _ in history if m == "neutral") / total * 100
            
            self.happy_stat.setText(f"Happy: {happy:.1f}%")
            self.sad_stat.setText(f"Sad: {sad:.1f}%")
            self.angry_stat.setText(f"Angry: {angry:.1f}%")
            self.neutral_stat.setText(f"Neutral: {neutral:.1f}%")
    
    def update_history(self, history):
        self.update_content(history)