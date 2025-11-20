from PySide6.QtWidgets import (QFrame, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QSizePolicy, QComboBox, QListWidgetItem, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from datetime import datetime
from api_client import APIClient

class HistoryPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_history_data = []
        self.setStyleSheet("background-color: #3a404d;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        title_layout = QHBoxLayout()
        title = QLabel("Mood History")
        title.setStyleSheet("QLabel { font-size: 24px; color: white; font-weight: bold; }")
        
        self.time_filter = QComboBox()
        self.time_filter.addItems(["Last 24 hours", "Last week", "Last month", "All time"])
        self.time_filter.setStyleSheet("""
            QComboBox {
                background-color: #5c6378; color: white; border: 1px solid #6c748c;
                border-radius: 8px; padding: 6px 12px; font-size: 14px; min-width: 50px;
            }
        """)
        
        export_button = QPushButton("Export Data")
        export_button.setIcon(QIcon(":/icons/export.png"))
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7; color: white; border: none;
                border-radius: 8px; padding: 8px 16px; font-size: 14px;
            }
            QPushButton:hover { background-color: #7d6ee8; }
        """)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(self.time_filter)
        title_layout.addWidget(export_button)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #424758; border-radius: 10px; padding: 10px;
                color: white; font-size: 14px; border: none;
            }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #5c6378; }
            QListWidget::item:selected { background-color: #6c5ce7; }
        """)
        
        stats_card = QFrame()
        stats_card.setStyleSheet("QFrame { background-color: #424758; border-radius: 15px; padding: 5px; }")
        stats_layout = QVBoxLayout(stats_card)
        
        stats_title = QLabel("📊 Mood Statistics")
        stats_title.setStyleSheet("""
            QLabel {
                font-size: 18px; color: white; font-weight: bold; padding-bottom: 5px;
            }
        """)
        
        # Correct emotion labels
        self.sleep_stat = QLabel("😴 Sleep: 0%")
        self.stress_stat = QLabel("😰 Stress: 0%")
        self.angry_stat = QLabel("😠 Angry: 0%")
        self.neutral_stat = QLabel("😐 Neutral: 0%")
        
        for label in [self.sleep_stat, self.stress_stat, self.angry_stat, self.neutral_stat]:
            label.setStyleSheet("font-size: 16px; color: #cccccc; padding: 5px;")
        
        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(self.sleep_stat)
        stats_layout.addWidget(self.stress_stat)
        stats_layout.addWidget(self.angry_stat)
        stats_layout.addWidget(self.neutral_stat)
        
        layout.addLayout(title_layout)
        layout.addWidget(self.history_list, 1)
        layout.addWidget(stats_card)

    def refresh_history(self):
        """Fetch latest mood history from API"""
        print("Refreshing mood history from backend...")
        # Assuming parent_window has user_id, default to 1 otherwise
        user_id = getattr(self.parent(), 'user_id', 1) 
        history_data = APIClient.get_mood_history(user_id)
        
        if isinstance(history_data, dict) and 'error' in history_data:
            QMessageBox.critical(self, "Error", str(history_data['error']))
            return

        # Sort data by timestamp, newest first
        self.all_history_data = sorted(history_data, key=lambda x: x.get('timestamp', ''), reverse=True)
        self.update_ui_with_data()
    
    def update_ui_with_data(self):
        """Populate list and stats"""
        self.history_list.clear()
        
        if not self.all_history_data:
            self.history_list.addItem("No mood history found.")
            return

        # Populate list
        for entry in self.all_history_data:
            mood = entry.get('mood', 'Unknown').capitalize()
            timestamp_str = entry.get('timestamp', '')
            source = entry.get('source', 'unknown')
            
            try:
                dt_object = datetime.fromisoformat(timestamp_str)
                display_time = dt_object.strftime('%Y-%m-%d %I:%M %p')
            except (ValueError, TypeError):
                display_time = "Invalid Date"

            # --- !!! LOGIC FIX: Cleaned up emojis to match your 4 emotions !!! ---
            mood_emojis = {
                'Sleep': '😴',
                'Sleepy': '😴', # Kept for safety
                'Stress': '😰',
                'Angry': '😠',
                'Neutral': '😐',
            }
            emoji = mood_emojis.get(mood, '😐')
            
            item_text = f"{emoji} {mood.ljust(12)} | {display_time} | {source}"
            list_item = QListWidgetItem(item_text)
            self.history_list.addItem(list_item)
            
        # Calculate statistics
        total = len(self.all_history_data)
        if total > 0:
            moods = [e.get('mood', 'neutral').lower() for e in self.all_history_data]
            
            # Count emotions (handle both 'sleep' and 'sleepy')
            # This is correct and matches your fusion logic
            sleep_count = moods.count("sleep") + moods.count("sleepy")
            stress_count = moods.count("stress")
            angry_count = moods.count("angry")
            neutral_count = moods.count("neutral")
            
            # Calculate percentages
            sleep_pct = sleep_count / total * 100
            stress_pct = stress_count / total * 100
            angry_pct = angry_count / total * 100
            neutral_pct = neutral_count / total * 100
            
            # Update labels with color coding
            self.sleep_stat.setText(f"😴 Sleep: {sleep_pct:.1f}%")
            self.sleep_stat.setStyleSheet(f"""
                font-size: 16px; padding: 5px;
                color: {'#9370DB' if sleep_pct > 0 else '#cccccc'};
                font-weight: {'bold' if sleep_pct > 30 else 'normal'};
            """)
            
            self.stress_stat.setText(f"😰 Stress: {stress_pct:.1f}%")
            self.stress_stat.setStyleSheet(f"""
                font-size: 16px; padding: 5px;
                color: {'#FF8C00' if stress_pct > 0 else '#cccccc'};
                font-weight: {'bold' if stress_pct > 30 else 'normal'};
            """)
            
            self.angry_stat.setText(f"😠 Angry: {angry_pct:.1f}%")
            self.angry_stat.setStyleSheet(f"""
                font-size: 16px; padding: 5px;
                color: {'#FF6347' if angry_pct > 0 else '#cccccc'};
                font-weight: {'bold' if angry_pct > 30 else 'normal'};
            """)
            
            self.neutral_stat.setText(f"😐 Neutral: {neutral_pct:.1f}%")
            self.neutral_stat.setStyleSheet(f"""
                font-size: 16px; padding: 5px;
                color: {'#98FB98' if neutral_pct > 0 else '#cccccc'};
                font-weight: {'bold' if neutral_pct > 30 else 'normal'};
            """)
            
            # Add warning if any emotion is too high
            if stress_pct > 50:
                self.stress_stat.setText(f"😰 Stress: {stress_pct:.1f}% ⚠️")
            if angry_pct > 50:
                self.angry_stat.setText(f"😠 Angry: {angry_pct:.1f}% ⚠️")
            if sleep_pct > 60:
                self.sleep_stat.setText(f"😴 Sleep: {sleep_pct:.1f}% ⚠️")