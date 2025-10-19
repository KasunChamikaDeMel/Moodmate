"""
MoodMate Main Application with Backend Integration
"""

from datetime import datetime, timedelta
import sys
import random
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QApplication
from PySide6.QtCore import QTimer
from ui_sidebar import Ui_MainWindow
from home import HomePage
from pet import PetPage
from detection import DetectionPage
from history import HistoryPage
from settings import SettingsPage
from profile_1 import ProfilePage
from help import HelpPage
from api_client import APIClient


class MoodMateApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("MoodMate - Your Emotional Companion")
        self.setMinimumSize(1000, 700)
        
        # Initialize variables
        self.current_mood = "neutral"
        self.pet_mood = "happy"
        self.username = "User"
        self.pet_name = "Buddy"
        self.user_id = 1
        
        # Check backend connection
        self.check_backend_connection()
        
        # Load initial data from backend
        self.load_user_data()
        self.load_pet_data()
        
        # Create page instances
        self.home_page = HomePage(self)
        self.pet_page = PetPage(self)
        self.detection_page = DetectionPage(self)
        self.history_page = HistoryPage(self)
        self.settings_page = SettingsPage(self)
        self.profile_page = ProfilePage(self)
        self.help_page = HelpPage(self)
        
        # Add pages to stacked widget
        self.stackedWidget.addWidget(self.home_page)
        self.stackedWidget.addWidget(self.pet_page)
        self.stackedWidget.addWidget(self.detection_page)
        self.stackedWidget.addWidget(self.history_page)
        self.stackedWidget.addWidget(self.settings_page)
        self.stackedWidget.addWidget(self.profile_page)
        self.stackedWidget.addWidget(self.help_page)
        
        # Setup sidebar
        self.icon_name_widgect.setHidden(True)
        self.connect_navigation()
        
        # Initialize pages with default values
        self.update_all_pages()
        
        # Setup timers
        self.setup_timers()
    
    def check_backend_connection(self):
        """Check if backend is running"""
        if not APIClient.test_connection():
            QMessageBox.warning(
                self,
                "Backend Connection",
                "⚠️ Cannot connect to backend server!\n\n"
                "Please ensure the backend is running:\n"
                "1. Open terminal in backend folder\n"
                "2. Run: python run.py\n\n"
                "The app will work with limited functionality."
            )
    
    def load_user_data(self):
        """Load user data from backend"""
        try:
            result = APIClient.get_user(self.user_id)
            if 'error' not in result:
                self.username = result.get('username', 'User')
        except Exception as e:
            print(f"Failed to load user data: {e}")
    
    def load_pet_data(self):
        """Load pet data from backend"""
        try:
            result = APIClient.get_pet_data(self.user_id)
            if 'error' not in result:
                self.pet_name = result.get('pet_name', 'Buddy')
                self.pet_mood = result.get('pet_mood', 'happy')
        except Exception as e:
            print(f"Failed to load pet data: {e}")
    
    def connect_navigation(self):
        """Connect all navigation buttons to their respective pages"""
        nav_map = {
            self.home_1: self.home_page,
            self.home_2: self.home_page,
            self.pet_1: self.pet_page,
            self.pet_2: self.pet_page,
            self.startdetection_1: self.detection_page,
            self.startdetection_2: self.detection_page,
            self.history_1: self.history_page,
            self.history_2: self.history_page,
            self.settings_1: self.settings_page,
            self.settings_2: self.settings_page,
            self.profile_1: self.profile_page,
            self.profile_2: self.profile_page,
            self.help_1: self.help_page,
            self.help_2: self.help_page
        }
        
        for button, page in nav_map.items():
            button.clicked.connect(lambda _, p=page: self.switch_page(p))
        
        # Set default page
        self.stackedWidget.setCurrentWidget(self.home_page)
        self.home_1.setChecked(True)
    
    def switch_page(self, page):
        """Switch to a page and refresh its data"""
        self.stackedWidget.setCurrentWidget(page)
        
        # Refresh data when switching to certain pages
        if page == self.history_page:
            self.history_page.refresh_history()
        elif page == self.pet_page:
            self.pet_page.refresh_data()
        elif page == self.profile_page:
            self.profile_page.load_user_data()
    
    def update_all_pages(self):
        """Update all pages with current data"""
        self.home_page.update_content(self.username, self.current_mood, self.pet_name)
        self.pet_page.update_content(self.pet_name, self.pet_mood)
        self.settings_page.update_content(self.pet_name)
        self.profile_page.update_content(self.username)
    
    def setup_timers(self):
        """Setup animation timer"""
        self.pet_animation_timer = QTimer(self)
        self.pet_animation_timer.timeout.connect(self.animate_pet)
        self.pet_animation_timer.start(300)
    
    def animate_pet(self):
        """Update pet animation on pet page"""
        if self.stackedWidget.currentWidget() == self.pet_page:
            self.pet_page.animate()
    
    def closeEvent(self, event):
        """Handle application close"""
        # Cleanup resources
        if hasattr(self.home_page, 'cleanup'):
            self.home_page.cleanup()
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MoodMateApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()