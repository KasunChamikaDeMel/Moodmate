"""
Profile Page with Backend Integration, Logout, and Statistics
"""

from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                              QLineEdit, QFormLayout, QSizePolicy, QSpacerItem, 
                              QPlainTextEdit, QScrollArea, QWidget, QGroupBox, QMessageBox)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap
from api_client import APIClient
from datetime import datetime


class ProfilePage(QFrame):
    """User profile page with logout and statistics"""
    
    logout_requested = Signal()
    profile_updated = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.user_id = 1
        self.user_data = {}
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
        
        # Title with logout button
        header_layout = QHBoxLayout()
        
        title = QLabel("👤 Your Profile")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                font-weight: bold;
            }
        """)
        
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        layout.addLayout(header_layout)
        
        # Avatar Section
        avatar_frame = QFrame()
        avatar_frame.setStyleSheet("""
            QFrame {
                background-color: #424758;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        avatar_layout = QHBoxLayout(avatar_frame)
        avatar_layout.setSpacing(20)
        
        # Avatar image
        self.avatar_label = QLabel("👤")
        self.avatar_label.setStyleSheet("""
            QLabel {
                font-size: 80px;
                background-color: #5c6378;
                border-radius: 60px;
                padding: 20px;
            }
        """)
        self.avatar_label.setFixedSize(120, 120)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # User info next to avatar
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(5)
        
        self.username_display = QLabel("Username")
        self.username_display.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        
        self.email_display = QLabel("email@example.com")
        self.email_display.setStyleSheet("font-size: 14px; color: #95a5a6;")
        
        self.joined_label = QLabel("Joined: --")
        self.joined_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        info_layout.addWidget(self.username_display)
        info_layout.addWidget(self.email_display)
        info_layout.addWidget(self.joined_label)
        info_layout.addStretch()
        
        avatar_layout.addWidget(self.avatar_label)
        avatar_layout.addWidget(info_widget, 1)
        
        layout.addWidget(avatar_frame)
        
        # Statistics Section
        stats_group = QGroupBox("📊 Your Statistics")
        stats_group.setStyleSheet("""
            QGroupBox {
                background-color: #424758;
                border: 1px solid #5c6378;
                border-radius: 10px;
                padding: 20px;
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
        
        stats_layout = QHBoxLayout(stats_group)
        stats_layout.setSpacing(15)
        
        # Mood entries stat
        self.mood_stat = self.create_stat_card("🎭", "Mood Entries", "0")
        stats_layout.addWidget(self.mood_stat)
        
        # Days active stat
        self.days_stat = self.create_stat_card("📅", "Days Active", "0")
        stats_layout.addWidget(self.days_stat)
        
        # Pet level stat
        self.pet_stat = self.create_stat_card("🐾", "Pet Level", "1")
        stats_layout.addWidget(self.pet_stat)
        
        layout.addWidget(stats_group)
        
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
        self.email_edit = self.create_form_field("Email:", form_layout, readonly=True)
        self.bio_edit = self.create_form_field("Bio:", form_layout, is_textarea=True)
        
        layout.addWidget(personal_group)
        
        # Button Row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.load_user_data)
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
        """)
        
        self.save_button = QPushButton("💾 Save Changes")
        self.save_button.clicked.connect(self.save_profile)
        self.save_button.setStyleSheet("""
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
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        main_layout.addWidget(scroll)
    
    def create_stat_card(self, icon, title, value):
        """Create a statistics card"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #5c6378;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setObjectName(f"stat_{title.lower().replace(' ', '_')}")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #95a5a6;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
    
    def create_form_field(self, label_text, form_layout, is_textarea=False, readonly=False):
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
        else:
            field = QLineEdit()
            if readonly:
                field.setReadOnly(True)
                field.setStyleSheet("""
                    QLineEdit {
                        background-color: #424758;
                        color: #95a5a6;
                        border: 1px solid #6c748c;
                        border-radius: 5px;
                        padding: 8px 12px;
                        font-size: 14px;
                    }
                """)
            else:
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
    
    def load_user_data(self, user_data=None):
        """Load user data from backend or provided dict"""
        if user_data:
            self.user_data = user_data
            self.user_id = user_data.get('id', 1)
        
        if not self.user_data:
            # Load from backend
            result = APIClient.get_user(self.user_id)
            if 'error' not in result:
                self.user_data = result
        
        if not self.user_data:
            print("No user data available")
            return
        
        # Update display fields
        username = self.user_data.get('username', 'User')
        email = self.user_data.get('email', 'user@example.com')
        
        self.username_display.setText(username)
        self.email_display.setText(email)
        
        # Parse joined date
        created_at = self.user_data.get('created_at', '')
        if created_at:
            try:
                date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                self.joined_label.setText(f"Joined: {date_obj.strftime('%B %d, %Y')}")
            except:
                self.joined_label.setText("Joined: Recently")
        
        # Update editable fields
        self.username_edit.setText(username)
        self.email_edit.setText(email)
        self.bio_edit.setPlainText(self.user_data.get('bio', ''))
        
        # Load statistics
        self.load_statistics()
        
        print(f"✅ Profile loaded for user: {username}")
    
    def load_statistics(self):
        """Load user statistics"""
        if not self.user_data:
            return
        
        user_id = self.user_data.get('id', 1)
        
        # Get mood history count
        try:
            history = APIClient.get_mood_history(user_id)
            if isinstance(history, list):
                mood_value = self.mood_stat.findChild(QLabel, "stat_mood_entries")
                if mood_value:
                    mood_value.setText(str(len(history)))
        except Exception as e:
            print(f"Error loading mood history: {e}")
        
        # Calculate days active
        created_at = self.user_data.get('created_at', '')
        if created_at:
            try:
                date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days = (datetime.now() - date_obj).days
                days_value = self.days_stat.findChild(QLabel, "stat_days_active")
                if days_value:
                    days_value.setText(str(max(1, days)))
            except Exception as e:
                print(f"Error calculating days: {e}")
        
        # Get pet level
        try:
            pet_data = APIClient.get_pet_data(user_id)
            if 'pet_level' in pet_data:
                pet_value = self.pet_stat.findChild(QLabel, "stat_pet_level")
                if pet_value:
                    pet_value.setText(str(pet_data['pet_level']))
        except Exception as e:
            print(f"Error loading pet data: {e}")
    
    def save_profile(self):
        """Save profile changes to backend"""
        if not self.user_data:
            QMessageBox.warning(self, "Error", "No user data loaded!")
            return
        
        try:
            # Collect data from form
            data = {
                'username': self.username_edit.text().strip(),
                'bio': self.bio_edit.toPlainText().strip()
            }
            
            # Validate
            if not data['username']:
                QMessageBox.warning(self, "Validation Error", "Username cannot be empty!")
                return
            
            # Send to backend
            result = APIClient.update_user(self.user_id, data)
            
            if 'error' in result:
                QMessageBox.warning(self, "Error", f"Failed to save profile: {result['error']}")
                return
            
            # Update local data
            self.user_data.update(data)
            self.username_display.setText(data['username'])
            
            # Emit signal
            self.profile_updated.emit(self.user_data)
            
            QMessageBox.information(self, "✅ Success", "Profile updated successfully!")
            print(f"✅ Profile updated: {data['username']}")
            
            # Update parent window username if it exists
            if self.parent_window and hasattr(self.parent_window, 'username'):
                self.parent_window.username = data['username']
                if hasattr(self.parent_window, 'home_page'):
                    self.parent_window.home_page.update_username(data['username'])
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save profile: {str(e)}")
    
    def logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear saved session
            import os
            if os.path.exists('user_session.json'):
                try:
                    os.remove('user_session.json')
                    print("✅ Session cleared")
                except Exception as e:
                    print(f"Error clearing session: {e}")
            
            print("✅ User logged out")
            self.logout_requested.emit()
    
    def update_content(self, username):
        """Legacy compatibility method"""
        if self.user_data:
            self.load_user_data()