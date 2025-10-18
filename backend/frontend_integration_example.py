"""
Frontend Integration Example for MoodMate
This file shows how to integrate your existing PySide6 frontend with the Flask backend
"""

import requests
import json
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtWidgets import QMessageBox

class BackendAPI:
    """Class to handle all backend API calls"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_connection(self):
        """Test if backend is accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_user_profile(self):
        """Get user profile from backend"""
        try:
            response = self.session.get(f"{self.base_url}/api/user/profile")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def update_user_profile(self, profile_data):
        """Update user profile in backend"""
        try:
            response = self.session.put(
                f"{self.base_url}/api/user/profile", 
                json=profile_data
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_pet_info(self):
        """Get pet information from backend"""
        try:
            response = self.session.get(f"{self.base_url}/api/pet/info")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def feed_pet(self):
        """Feed the pet via backend"""
        try:
            response = self.session.post(f"{self.base_url}/api/pet/feed")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def play_with_pet(self):
        """Play with the pet via backend"""
        try:
            response = self.session.post(f"{self.base_url}/api/pet/play")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_current_mood(self):
        """Get current mood from backend"""
        try:
            response = self.session.get(f"{self.base_url}/api/mood/current")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def add_mood_entry(self, mood, notes=""):
        """Add mood entry to backend"""
        try:
            data = {"mood": mood, "notes": notes}
            response = self.session.post(f"{self.base_url}/api/mood/history", json=data)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_mood_history(self):
        """Get mood history from backend"""
        try:
            response = self.session.get(f"{self.base_url}/api/mood/history")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

class BackendSyncThread(QThread):
    """Thread for syncing data with backend in background"""
    
    sync_completed = Signal(dict)
    sync_error = Signal(str)
    
    def __init__(self, api, sync_type, data=None):
        super().__init__()
        self.api = api
        self.sync_type = sync_type
        self.data = data
    
    def run(self):
        """Run the sync operation"""
        try:
            if self.sync_type == "profile":
                result = self.api.get_user_profile()
            elif self.sync_type == "pet":
                result = self.api.get_pet_info()
            elif self.sync_type == "mood":
                result = self.api.get_current_mood()
            elif self.sync_type == "history":
                result = self.api.get_mood_history()
            else:
                result = None
            
            if result:
                self.sync_completed.emit(result)
            else:
                self.sync_error.emit(f"Failed to sync {self.sync_type}")
                
        except Exception as e:
            self.sync_error.emit(str(e))

class BackendIntegration:
    """Main integration class for your frontend"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.api = BackendAPI()
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.sync_with_backend)
        
        # Check backend connection
        if not self.api.test_connection():
            self.show_backend_warning()
        else:
            self.start_backend_sync()
    
    def show_backend_warning(self):
        """Show warning if backend is not accessible"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Backend Connection Failed")
        msg.setInformativeText(
            "Cannot connect to MoodMate backend.\n"
            "The app will run in offline mode.\n\n"
            "To enable backend features:\n"
            "1. Start the Flask backend (python app.py)\n"
            "2. Restart this application"
        )
        msg.setWindowTitle("Backend Warning")
        msg.exec()
    
    def start_backend_sync(self):
        """Start periodic backend synchronization"""
        self.sync_timer.start(30000)  # Sync every 30 seconds
        self.sync_with_backend()  # Initial sync
    
    def sync_with_backend(self):
        """Synchronize data with backend"""
        # Sync user profile
        profile_thread = BackendSyncThread(self.api, "profile")
        profile_thread.sync_completed.connect(self.update_user_profile)
        profile_thread.sync_error.connect(self.handle_sync_error)
        profile_thread.start()
        
        # Sync pet info
        pet_thread = BackendSyncThread(self.api, "pet")
        pet_thread.sync_completed.connect(self.update_pet_info)
        pet_thread.sync_error.connect(self.handle_sync_error)
        pet_thread.start()
        
        # Sync mood data
        mood_thread = BackendSyncThread(self.api, "mood")
        mood_thread.sync_completed.connect(self.update_mood_data)
        mood_thread.sync_error.connect(self.handle_sync_error)
        mood_thread.start()
    
    def update_user_profile(self, profile_data):
        """Update frontend with user profile from backend"""
        if hasattr(self.main_window, 'username'):
            self.main_window.username = profile_data.get('username', 'User')
        if hasattr(self.main_window, 'update_all_pages'):
            self.main_window.update_all_pages()
    
    def update_pet_info(self, pet_data):
        """Update frontend with pet info from backend"""
        if hasattr(self.main_window, 'pet_name'):
            self.main_window.pet_name = pet_data.get('pet_name', 'Buddy')
        if hasattr(self.main_window, 'pet_mood'):
            self.main_window.pet_mood = pet_data.get('pet_mood', 'happy')
        if hasattr(self.main_window, 'update_all_pages'):
            self.main_window.update_all_pages()
    
    def update_mood_data(self, mood_data):
        """Update frontend with mood data from backend"""
        if hasattr(self.main_window, 'current_mood'):
            self.main_window.current_mood = mood_data.get('current_mood', 'neutral')
        if hasattr(self.main_window, 'update_all_pages'):
            self.main_window.update_all_pages()
    
    def handle_sync_error(self, error_message):
        """Handle backend sync errors"""
        print(f"Backend sync error: {error_message}")
        # You can add error handling UI here
    
    def feed_pet(self):
        """Feed pet via backend"""
        result = self.api.feed_pet()
        if result:
            self.update_pet_info(result)
            return True
        return False
    
    def play_with_pet(self):
        """Play with pet via backend"""
        result = self.api.play_with_pet()
        if result:
            self.update_pet_info(result)
            return True
        return False
    
    def add_mood(self, mood, notes=""):
        """Add mood entry via backend"""
        result = self.api.add_mood_entry(mood, notes)
        if result:
            # Refresh mood data
            self.sync_with_backend()
            return True
        return False

# Example of how to integrate this into your existing MoodMateApp class
"""
# In your sidebar.py file, add this integration:

from frontend_integration_example import BackendIntegration

class MoodMateApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ... your existing initialization code ...
        
        # Add backend integration
        self.backend = BackendIntegration(self)
        
        # ... rest of your initialization code ...
    
    def feed_pet_action(self):
        # Replace your existing pet feeding logic with:
        if self.backend.feed_pet():
            # Success - pet was fed via backend
            pass
        else:
            # Fallback to local logic
            self.pet_mood = "happy"
            self.update_all_pages()
    
    def add_mood_entry(self, mood, notes=""):
        # Replace your existing mood logic with:
        if self.backend.add_mood(mood, notes):
            # Success - mood saved to backend
            pass
        else:
            # Fallback to local logic
            mood_entry = {
                "mood": mood,
                "timestamp": datetime.now(),
                "notes": notes
            }
            self.mood_history.append(mood_entry)
            self.update_all_pages()
"""
