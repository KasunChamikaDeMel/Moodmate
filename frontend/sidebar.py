

from datetime import datetime
import sys
import json
import os
import threading
import subprocess
import platform
import requests
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QApplication
from PySide6.QtCore import QTimer, Slot
from PySide6.QtCore import QThreadPool
from ui_sidebar import Ui_MainWindow
from home import HomePage
from history import HistoryPage
from profile_1 import ProfilePage
from help import HelpPage
from api_client import APIClient
from auth import AuthenticationWidget
from theme_manager import ThemeManager
from worker import Worker

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
        # Connect header search and profile buttons
        try:
            self.lineEdit.returnPressed.connect(self.on_search)
            self.pushButton_18.clicked.connect(self.on_search)
        except Exception:
            pass
        try:
            self.profile_3.clicked.connect(lambda: self.switch_page(self.profile_page))
        except Exception:
            pass
        
        # Setup sidebar
        self.icon_name_widgect.setHidden(True)
        self.connect_navigation()
        
        # Connect home page emotion detection to notifications
        self.connect_emotion_signals()
        
        # Initialize pages with default values
        self.update_all_pages()
        
        # Setup timers
        self.setup_timers()
        
        # Pet app should already be running (started with backend)
        # No need to start it here

        # Apply initial global dark theme across all pages for consistency
        try:
            self.apply_theme_to_all("Dark")
        except Exception as e:
            print(f"Initial theme apply failed: {e}")
    
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

        # Also load user settings from backend asynchronously to avoid blocking UI
        def _load_user_settings(user_id):
            return APIClient.get_user_settings(user_id)

        worker = Worker(_load_user_settings, getattr(self, 'user_id', 1))
        worker.signals.result.connect(self._apply_loaded_user_settings)
        worker.signals.error.connect(lambda e: print(f"Error loading user settings: {e}"))
        QThreadPool.globalInstance().start(worker)

    @Slot(object)
    def _apply_loaded_user_settings(self, result):
        if isinstance(result, dict) and 'theme' in result:
            # apply theme preference non-blocking
            try:
                app = QApplication.instance()
                if app:
                    from theme_manager import ThemeManager
                    ThemeManager.apply_theme(app, result.get('theme', 'Dark'))
            except Exception:
                pass
    
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
        
        # Get duration from notification settings
        try:
            settings = self.notification_settings_page.get_current_settings()
            duration = settings.get('duration', 20)  # Default 20 seconds
        except:
            duration = 20  # Fallback to 20 seconds
        
        # Show notification with duration from settings
        self.notification_window.show_notification(emotion, "detection", duration=duration)
        
        print(f"🔔 Notification shown for: {emotion} (duration: {duration}s)")
    
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
        print(f"Theme changed to: {theme_name}")
        try:
            self.apply_theme_to_all(theme_name)
            print(f"Global theme applied: {theme_name}")
        except Exception as e:
            print(f"Failed to apply global theme: {e}")

    def apply_theme_to_all(self, theme_name):
        """Apply ThemeManager stylesheet and allow pages to adjust local elements."""
        app = QApplication.instance()
        if app is None:
            return
        ThemeManager.apply_theme(app, theme_name)
        # Propagate to pages that expose local apply hooks
        for page in [
            getattr(self, 'home_page', None),
            getattr(self, 'pet_page', None),
            getattr(self, 'notification_settings_page', None),
            getattr(self, 'history_page', None),
            getattr(self, 'settings_page', None),
            getattr(self, 'profile_page', None),
            getattr(self, 'help_page', None)
        ]:
            if page is None:
                continue
            # Prefer explicit local theme method names
            try:
                if hasattr(page, 'apply_theme_local'):
                    page.apply_theme_local(theme_name)
                elif hasattr(page, 'apply_styles'):
                    page.apply_styles(theme_name)
            except Exception as e:
                print(f"Theme propagate failed for {page}: {e}")
    
    def on_notification_settings_changed(self, settings):
        """Handle notification settings changes"""
        self.notifications_enabled = settings.get('enabled', True)
        self.pet_type = settings.get('pet_type', 'cat')
        self.notification_window.set_pet_type(self.pet_type)
        print(f"🔔 Notification settings updated: {settings}")

    def on_search(self):
        """Handle header search: query mood history and show results in History page."""
        query = ''
        try:
            query = self.lineEdit.text().strip()
        except Exception:
            pass

        if not query:
            QMessageBox.information(self, "Search", "Please enter a search term (mood or date).")
            return

        # Fetch full history in background and filter locally when ready
        def _fetch_history(uid):
            return APIClient.get_mood_history(uid)

        worker = Worker(_fetch_history, self.user_id)
        worker.signals.result.connect(lambda all_history: self._handle_search_results(query, all_history))
        worker.signals.error.connect(lambda err: QMessageBox.critical(self, "Search Error", f"Failed to fetch history: {err}"))
        QThreadPool.globalInstance().start(worker)

    @Slot(str, object)
    def _handle_search_results(self, query, all_history):
        try:
            if isinstance(all_history, dict) and 'error' in all_history:
                QMessageBox.critical(self, "Search Error", f"Failed to fetch history: {all_history.get('error')}")
                return

            q = query.lower()
            filtered = []
            for e in all_history:
                mood = str(e.get('mood', '')).lower()
                source = str(e.get('source', '')).lower()
                ts = str(e.get('timestamp', '')).lower()
                if q in mood or q in source or q in ts:
                    filtered.append(e)

            if not filtered:
                QMessageBox.information(self, "Search", f"No results for '{query}'")
                return

            self.history_page.all_history_data = sorted(filtered, key=lambda x: x.get('timestamp', ''), reverse=True)
            self.switch_page(self.history_page)
            self.history_page.update_ui_with_data()
        except Exception as ex:
            QMessageBox.critical(self, "Search Error", f"An error occurred: {str(ex)}")
    
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
        # Load user data in background to avoid blocking UI
        def _get_user(uid):
            return APIClient.get_user(uid)

        worker = Worker(_get_user, self.user_id)
        worker.signals.result.connect(self._apply_user_data)
        worker.signals.error.connect(lambda e: print(f"Failed to load user data: {e}"))
        QThreadPool.globalInstance().start(worker)

    @Slot(object)
    def _apply_user_data(self, result):
        try:
            if isinstance(result, dict) and 'error' not in result:
                self.username = result.get('username', 'User')
                print(f"Loaded user: {self.username}")
                # update home page username if present
                if hasattr(self, 'home_page'):
                    self.home_page.update_username(self.username)
        except Exception as e:
            print(f"Error applying user data: {e}")
    
    def load_pet_data(self):
        """Load pet data from backend"""
        # Load pet data in background to avoid blocking UI
        def _get_pet(uid):
            return APIClient.get_pet_data(uid)

        worker = Worker(_get_pet, self.user_id)
        worker.signals.result.connect(self._apply_pet_data)
        worker.signals.error.connect(lambda e: print(f"Failed to load pet data: {e}"))
        QThreadPool.globalInstance().start(worker)

    @Slot(object)
    def _apply_pet_data(self, result):
        try:
            if isinstance(result, dict) and 'error' not in result:
                self.pet_name = result.get('pet_name', 'Buddy')
                self.pet_type = result.get('pet_type', 'cat')
                self.pet_mood = result.get('pet_mood', 'happy')
                print(f"Loaded pet: {self.pet_name} ({self.pet_type}) - mood: {self.pet_mood}")
                # Update UI pages if they exist
                if hasattr(self, 'pet_page'):
                    self.pet_page.pet_name = self.pet_name
                    self.pet_page.pet_type = self.pet_type
                    self.pet_page.update_ui()
        except Exception as e:
            print(f"Error applying pet data: {e}")
    
    def connect_navigation(self):
        """Connect all navigation buttons to their respective pages"""
        nav_map = {
            self.home_1: self.home_page,
            self.home_2: self.home_page,
            self.pet_1: self.pet_page,
            self.pet_2: self.pet_page,
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
        """Handle application close safely"""
        try:
            if hasattr(self, 'home_page') and self.home_page:
                if hasattr(self.home_page, 'cleanup'):
                    self.home_page.cleanup()
        except Exception as e:
            print(f"Home cleanup error: {e}")
        
        try:
            if hasattr(self, 'notification_window') and self.notification_window:
                self.notification_window.close()
        except Exception as e:
            print(f"Notification cleanup error: {e}")
        
        try:
            if hasattr(self, 'pet_animation_timer') and self.pet_animation_timer:
                self.pet_animation_timer.stop()
        except Exception as e:
            print(f"Timer cleanup error: {e}")
        
        event.accept()
    
    def check_pet_app_running(self):
        """Check if pet app is running by testing ports (non-blocking with short timeout)"""
        ports_to_try = [4000, 4001, 4002, 4003, 4004, 4005]
        for port in ports_to_try:
            try:
                # Try a GET request with very short timeout (non-blocking)
                response = requests.get(f"http://localhost:{port}/trigger", timeout=0.1)
                return True
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.Timeout:
                continue
            except:
                # Any response (even error) means server is running
                return True
        return False
    
    def start_pet_app_once(self):
        """Start Electron pet app once at application startup (in background thread)"""
        # Start in background thread (completely non-blocking)
        thread = threading.Thread(target=self._start_pet_app_background, daemon=True)
        thread.start()
    
    def _start_pet_app_background(self):
        """Background thread function to start pet app (completely non-blocking)"""
        # Quick check first (with minimal timeout)
        if self.check_pet_app_running():
            print("🐾 Pet app is already running")
            return
        
        try:
            # Get the project root directory (go up from frontend/)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            pet_dir = os.path.join(project_root, 'moodmate-pet')
            
            if not os.path.exists(pet_dir):
                print(f"⚠️ Pet app directory not found: {pet_dir}")
                return False
            
            # Check if node_modules exists (dependencies installed)
            node_modules = os.path.join(pet_dir, 'node_modules')
            if not os.path.exists(node_modules):
                print("⚠️ Pet app dependencies not installed. Please run 'npm install' in moodmate-pet directory")
                return False
            
            # Start Electron app silently in background (no CMD window)
            if platform.system() == 'Windows':
                # On Windows, use start /B to run in background without showing CMD window
                subprocess.Popen(
                    ['cmd', '/c', 'start', '/B', 'npm', 'start'],
                    cwd=pet_dir,
                    shell=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
            else:
                # On Linux/Mac
                subprocess.Popen(
                    ['npm', 'start'],
                    cwd=pet_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            
            print("🚀 Starting Electron pet app in background (once at startup)...")
            print("   (The HTTP server will start on port 4000)")
            
            # Check if it started successfully (with retries in background)
            import time
            for i in range(10):  # Check 10 times over 5 seconds
                time.sleep(0.5)  # Check every 0.5 seconds
                if self.check_pet_app_running():
                    print("✅ Pet app started successfully")
                    return True
            
            print("⚠️ Pet app may still be starting. It will be ready when needed.")
            return False
                
        except Exception as e:
            print(f"❌ Error starting pet app: {e}")
            return False


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MoodMateApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()