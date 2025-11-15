"""
Authentication System for MoodMate
Place this in: frontend/auth.py
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QLineEdit, QFrame, QMessageBox,
                              QCheckBox, QStackedWidget)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont
from api_client import APIClient
import hashlib
import json
import os


class AuthenticationWidget(QWidget):
    """Main authentication widget with login and registration"""
    
    login_successful = Signal(dict)  # Emits user data on successful login
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the authentication UI"""
        self.setStyleSheet("background-color: #2c3e50;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget for login/register pages
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #2c3e50;")
        
        # Create pages
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        
        # Connect signals
        self.login_page.login_successful.connect(self.on_login_success)
        self.login_page.switch_to_register.connect(lambda: self.stack.setCurrentWidget(self.register_page))
        self.register_page.registration_successful.connect(self.on_registration_success)
        self.register_page.switch_to_login.connect(lambda: self.stack.setCurrentWidget(self.login_page))
        
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        
        layout.addWidget(self.stack)
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.login_successful.emit(user_data)
        print(f"✅ User logged in: {user_data['username']}")
    
    def on_registration_success(self):
        """Handle successful registration"""
        self.stack.setCurrentWidget(self.login_page)
        QMessageBox.information(self, "✅ Success", 
            "Registration successful!\nPlease login with your credentials.")


class LoginPage(QWidget):
    """Login page"""
    
    login_successful = Signal(dict)
    switch_to_register = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup login UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login container
        container = QFrame()
        container.setMaximumWidth(450)
        container.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 20px;
                padding: 40px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Logo/Title
        title = QLabel("🌟 MoodMate")
        title.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #3498db;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        subtitle = QLabel("Your Emotional Companion")
        subtitle.setStyleSheet("font-size: 16px; color: #95a5a6; padding-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(subtitle)
        
        # Email field
        email_label = QLabel("📧 Email")
        email_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold;")
        container_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #5dade2;
            }
        """)
        container_layout.addWidget(self.email_input)
        
        # Password field
        password_label = QLabel("🔒 Password")
        password_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold; margin-top: 10px;")
        container_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #5dade2;
            }
        """)
        self.password_input.returnPressed.connect(self.login)
        container_layout.addWidget(self.password_input)
        
        # Remember me
        self.remember_check = QCheckBox("Remember me")
        self.remember_check.setStyleSheet("""
            QCheckBox {
                color: #95a5a6;
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #3498db;
                background-color: #2c3e50;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
            }
        """)
        container_layout.addWidget(self.remember_check)
        
        # Login button
        login_btn = QPushButton("🚀 Login")
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        container_layout.addWidget(login_btn)
        
        # Register link
        register_container = QWidget()
        register_layout = QHBoxLayout(register_container)
        register_layout.setContentsMargins(0, 10, 0, 0)
        
        register_label = QLabel("Don't have an account?")
        register_label.setStyleSheet("color: #95a5a6; font-size: 13px;")
        
        register_btn = QPushButton("Register here")
        register_btn.clicked.connect(self.switch_to_register.emit)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498db;
                border: none;
                font-size: 13px;
                font-weight: bold;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #5dade2;
            }
        """)
        
        register_layout.addStretch()
        register_layout.addWidget(register_label)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        
        container_layout.addWidget(register_container)
        
        layout.addWidget(container)
        
        # Load saved credentials
        self.load_credentials()
    
    def login(self):
        """Handle login"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "❌ Error", "Please enter both email and password!")
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Authenticate with backend
        result = APIClient.login(email, password_hash)
        
        if 'error' in result:
            QMessageBox.critical(self, "❌ Login Failed", 
                f"Invalid email or password!\n\n{result['error']}")
        else:
            # Save credentials if remember me is checked
            if self.remember_check.isChecked():
                self.save_credentials(email)
            else:
                self.clear_saved_credentials()
            
            self.login_successful.emit(result)
    
    def save_credentials(self, email):
        """Save email for remember me"""
        try:
            with open('user_session.json', 'w') as f:
                json.dump({'email': email}, f)
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
    def load_credentials(self):
        """Load saved credentials"""
        try:
            if os.path.exists('user_session.json'):
                with open('user_session.json', 'r') as f:
                    data = json.load(f)
                    self.email_input.setText(data.get('email', ''))
                    self.remember_check.setChecked(True)
        except Exception as e:
            print(f"Error loading credentials: {e}")
    
    def clear_saved_credentials(self):
        """Clear saved credentials"""
        try:
            if os.path.exists('user_session.json'):
                os.remove('user_session.json')
        except Exception as e:
            print(f"Error clearing credentials: {e}")


class RegisterPage(QWidget):
    """Registration page"""
    
    registration_successful = Signal()
    switch_to_login = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup registration UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Register container
        container = QFrame()
        container.setMaximumWidth(450)
        container.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 20px;
                padding: 40px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Title
        title = QLabel("✨ Create Account")
        title.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #3498db;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)
        
        # Username field
        username_label = QLabel("👤 Username")
        username_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold;")
        container_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setStyleSheet(self.input_style())
        container_layout.addWidget(self.username_input)
        
        # Email field
        email_label = QLabel("📧 Email")
        email_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold; margin-top: 10px;")
        container_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet(self.input_style())
        container_layout.addWidget(self.email_input)
        
        # Password field
        password_label = QLabel("🔒 Password")
        password_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold; margin-top: 10px;")
        container_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.input_style())
        container_layout.addWidget(self.password_input)
        
        # Confirm password field
        confirm_label = QLabel("🔒 Confirm Password")
        confirm_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold; margin-top: 10px;")
        container_layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setStyleSheet(self.input_style())
        self.confirm_input.returnPressed.connect(self.register)
        container_layout.addWidget(self.confirm_input)
        
        # Register button
        register_btn = QPushButton("🎉 Create Account")
        register_btn.clicked.connect(self.register)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)
        container_layout.addWidget(register_btn)
        
        # Login link
        login_container = QWidget()
        login_layout = QHBoxLayout(login_container)
        login_layout.setContentsMargins(0, 10, 0, 0)
        
        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet("color: #95a5a6; font-size: 13px;")
        
        login_btn = QPushButton("Login here")
        login_btn.clicked.connect(self.switch_to_login.emit)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498db;
                border: none;
                font-size: 13px;
                font-weight: bold;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #5dade2;
            }
        """)
        
        login_layout.addStretch()
        login_layout.addWidget(login_label)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()
        
        container_layout.addWidget(login_container)
        
        layout.addWidget(container)
    
    def input_style(self):
        """Return input field style"""
        return """
            QLineEdit {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #27ae60;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2ecc71;
            }
        """
    
    def register(self):
        """Handle registration"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validation
        if not username or not email or not password:
            QMessageBox.warning(self, "❌ Error", "Please fill in all fields!")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "❌ Error", "Username must be at least 3 characters!")
            return
        
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "❌ Error", "Please enter a valid email!")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "❌ Error", "Password must be at least 6 characters!")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "❌ Error", "Passwords do not match!")
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Register with backend
        result = APIClient.register(username, email, password_hash)
        
        if 'error' in result:
            QMessageBox.critical(self, "❌ Registration Failed", 
                f"Could not create account!\n\n{result['error']}")
        else:
            self.registration_successful.emit()
            # Clear fields
            self.username_input.clear()
            self.email_input.clear()
            self.password_input.clear()
            self.confirm_input.clear()