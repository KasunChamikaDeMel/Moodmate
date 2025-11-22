

from datetime import datetime
import sys
import json
import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QApplication
from PySide6.QtCore import QTimer
from ui_sidebar import Ui_MainWindow
from home import HomePage
from history import HistoryPage
from profile_1 import ProfilePage
from help import HelpPage
from api_client import APIClient
from auth import AuthenticationWidget
from theme_manager import ThemeManager

# Import notification components
from notification_widget import WindowsToastNotification
from notification_settings import NotificationSettingsPage
from settings import SettingsPage
from pet import PetPage


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
        self.pet_type = "cat"
        self.user_id = 1
        
        # Settings
        self.notifications_enabled = True
        self.notification_sounds = True
        
        # Create Windows-style notification window
        self.notification_window = WindowsToastNotification(self)
        self.notification_window.action_clicked.connect(self.handle_notification_action)
        
        # Check backend connection
        self.check_backend_connection()
        
        # Load initial data from backend and settings
        self.load_settings()
        self.load_user_data()
        self.load_pet_data()
        
        self.home_page = HomePage(self)
        self.pet_page = PetPage(self) 
        self.notification_settings_page = NotificationSettingsPage(self)
        self.history_page = HistoryPage(self)
        self.settings_page = SettingsPage(self)
        self.profile_page = ProfilePage(self)
        self.help_page = HelpPage(self)
        
        # Add pages to stacked widget
        self.stackedWidget.addWidget(self.home_page)
        self.stackedWidget.addWidget(self.pet_page)
        self.stackedWidget.addWidget(self.notification_settings_page)
        self.stackedWidget.addWidget(self.history_page)
        self.stackedWidget.addWidget(self.settings_page)
        self.stackedWidget.addWidget(self.profile_page)
        self.stackedWidget.addWidget(self.help_page)
        
        # Connect settings signals
        self.settings_page.pet_changed.connect(self.on_pet_changed)
        self.settings_page.theme_changed.connect(self.on_theme_changed)
        self.notification_settings_page.settings_changed.connect(self.on_notification_settings_changed)
        
        # Setup sidebar
        self.icon_name_widgect.setHidden(True)
        self.connect_navigation()
        
        # Connect home page emotion detection to notifications
        self.connect_emotion_signals()
        
        # Initialize pages with default values
        self.update_all_pages()
        
        # Setup timers
        self.setup_timers()
    
    def load_settings(self):
        """Load app settings from file"""
        settings_file = "settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                self.notifications_enabled = settings.get('enable_notifications', True)
                self.notification_sounds = settings.get('sound_notifications', True)
                self.pet_type = settings.get('pet_type', 'cat')
                print(f"✅ Settings loaded: Notifications={self.notifications_enabled}, Pet={self.pet_type}")
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def connect_emotion_signals(self):
        """Connect emotion detection to notification system"""
        original_update_emotion = self.home_page.update_emotion
        
        def wrapped_update_emotion(emotion):
            # Call original method
            original_update_emotion(emotion)
            
            # Show notification for negative emotions
            if self.notifications_enabled:
                emotion_lower = emotion.lower().strip()
                print(f"🔍 Checking notification for emotion: {emotion_lower}")
                
                # Normalize emotion names (fusion returns 'sleep' but notification uses 'sleepy')
                emotion_map = {
                    'sleep': 'sleepy',
                    'anger': 'angry'
                }
                normalized_emotion = emotion_map.get(emotion_lower, emotion_lower)
                
                # Check if this emotion should trigger notifications
                if normalized_emotion in ['stress', 'angry', 'sleepy']:
                    # Get current notification settings to check triggers
                    try:
                        settings = self.notification_settings_page.get_current_settings()
                        print(f"🔍 Notification settings - stress: {settings.get('trigger_stress')}, angry: {settings.get('trigger_angry')}, sleepy: {settings.get('trigger_sleepy')}")
                        
                        # Check if this specific emotion trigger is enabled
                        trigger_map = {
                            'stress': settings.get('trigger_stress', True),
                            'angry': settings.get('trigger_angry', True),
                            'sleepy': settings.get('trigger_sleepy', True)
                        }
                        
                        should_trigger = trigger_map.get(normalized_emotion, False)
                        print(f"🔍 Should trigger notification for {normalized_emotion}: {should_trigger}")
                        
                        if should_trigger:
                            self.show_emotion_notification(normalized_emotion)
                        else:
                            print(f"🔕 Notification skipped for {normalized_emotion} (trigger disabled in settings)")
                    except Exception as e:
                        # Fallback: show notification if settings can't be read
                        print(f"⚠️ Error reading notification settings: {e}, showing notification anyway")
                        import traceback
                        traceback.print_exc()
                        self.show_emotion_notification(normalized_emotion)
                else:
                    print(f"🔕 Emotion {normalized_emotion} not in notification list (stress/angry/sleepy)")
        
        self.home_page.update_emotion = wrapped_update_emotion
    
    def show_emotion_notification(self, emotion):
        """Show Windows-style toast notification for detected emotion"""
        # Emotion is already normalized when passed here
        # Set the pet type in notification
        self.notification_window.set_pet_type(self.pet_type)
        
        # Show notification
        self.notification_window.show_notification(emotion, "detection")
        
        print(f"🔔 Notification shown for: {emotion}")
    
    def handle_notification_action(self, action):
        """Handle notification button clicks"""
        if action == "better":
            print("✅ User feeling better!")
            try:
                APIClient.add_mood_entry(1, "improved", "user_action")
            except:
                pass
        elif action == "help":
            print("ℹ️ User wants more help")
            self.switch_page(self.help_page)
    
    def on_pet_changed(self, pet_name, pet_type):
        """Handle pet changes from settings"""
        self.pet_name = pet_name
        self.pet_type = pet_type
        
        # Update notification window
        self.notification_window.set_pet_type(pet_type)
        
        # Update pet page
        if hasattr(self, 'pet_page'):
            self.pet_page.pet_name = pet_name
            self.pet_page.pet_type = pet_type
            self.pet_page.update_ui()
        
        # Update home page
        if hasattr(self, 'home_page'):
            self.home_page.update_username(self.username)
        
        print(f"🐾 Pet updated: {pet_name} ({pet_type})")
    
    def on_theme_changed(self, theme_name):
        """Handle theme changes"""
        print(f"🎨 Theme changed to: {theme_name}")
    
    def on_notification_settings_changed(self, settings):
        """Handle notification settings changes"""
        self.notifications_enabled = settings.get('enabled', True)
        self.pet_type = settings.get('pet_type', 'cat')
        self.notification_window.set_pet_type(self.pet_type)
        print(f"🔔 Notification settings updated: {settings}")
    
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
                print(f"✅ Loaded user: {self.username}")
        except Exception as e:
            print(f"Failed to load user data: {e}")
    
    def load_pet_data(self):
        """Load pet data from backend"""
        try:
            result = APIClient.get_pet_data(self.user_id)
            if 'error' not in result:
                self.pet_name = result.get('pet_name', 'Buddy')
                self.pet_type = result.get('pet_type', 'cat')
                self.pet_mood = result.get('pet_mood', 'happy')
                print(f"✅ Loaded pet: {self.pet_name} ({self.pet_type}) - mood: {self.pet_mood}")
        except Exception as e:
            print(f"Failed to load pet data: {e}")
    
    def connect_navigation(self):
        """Connect all navigation buttons to their respective pages"""
        nav_map = {
            self.home_1: self.home_page,
            self.home_2: self.home_page,
            self.pet_1: self.pet_page,
            self.pet_2: self.pet_page,
            # NOTIFICATION SETTINGS PAGE (replaces detection)
            self.startdetection_1: self.notification_settings_page,
            self.startdetection_2: self.notification_settings_page,
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
        elif page == self.settings_page:
            self.settings_page.load_settings()
        elif page == self.notification_settings_page:
            self.notification_settings_page.load_settings()
    
    def update_all_pages(self):
        """Update all pages with current data"""
        self.home_page.update_content(self.username, self.current_mood, self.pet_name)
        self.pet_page.pet_name = self.pet_name
        self.pet_page.pet_type = self.pet_type
        self.pet_page.update_ui()
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
            pass
    
    def closeEvent(self, event):
        """Handle application close"""
        if hasattr(self.home_page, 'cleanup'):
            self.home_page.cleanup()
        
        if hasattr(self, 'notification_window'):
            self.notification_window.close()
        
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MoodMateApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()