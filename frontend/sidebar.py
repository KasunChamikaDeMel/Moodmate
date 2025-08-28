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
        self.mood_history = []
        self.generate_sample_history()
        
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
            button.clicked.connect(lambda _, p=page: self.stackedWidget.setCurrentWidget(p))
        
        # Set default page
        self.stackedWidget.setCurrentWidget(self.home_page)
        self.home_1.setChecked(True)
    
    def update_all_pages(self):
        """Update all pages with current data"""
        self.home_page.update_content(self.username, self.current_mood, self.pet_name)
        self.pet_page.update_content(self.pet_name, self.pet_mood)
        self.history_page.update_content(self.mood_history)
        self.settings_page.update_content(self.pet_name)
        self.profile_page.update_content(self.username)
    
    def setup_timers(self):
        """Setup animation and mood update timers"""
        self.pet_animation_timer = QTimer(self)
        self.pet_animation_timer.timeout.connect(self.animate_pet)
        self.pet_animation_timer.start(300)
        
        self.mood_update_timer = QTimer(self)
        self.mood_update_timer.timeout.connect(self.simulate_mood_change)
        self.mood_update_timer.start(10000)
    
    def animate_pet(self):
        """Update pet animation on pet page"""
        self.pet_page.animate()
    
    def simulate_mood_change(self):
        """Simulate mood changes for demo purposes"""
        moods = ["happy", "sad", "angry", "neutral"]
        new_mood = random.choice(moods)
        
        if new_mood != self.current_mood:
            self.current_mood = new_mood
            self.mood_history.append((self.current_mood, datetime.now().strftime("%H:%M %m/%d")))
            
            # Pet reacts to your mood
            pet_reactions = {
                "happy": "happy",
                "sad": "sad",
                "angry": "angry",
                "neutral": "happy"
            }
            self.pet_mood = pet_reactions.get(self.current_mood, "happy")
            
            # Update all affected pages
            self.home_page.update_mood(self.current_mood)
            self.pet_page.update_mood(self.pet_mood)
            self.history_page.update_history(self.mood_history)
    
    def generate_sample_history(self):
        """Generate some sample mood history"""
        moods = ["happy", "sad", "angry", "neutral"]
        now = datetime.now()
        for i in range(10):
            time = now - timedelta(hours=i)
            self.mood_history.append((random.choice(moods), time.strftime("%H:%M %m/%d")))