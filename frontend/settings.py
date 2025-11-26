"""
Settings Page - Functional with Backend Integration
Pet settings removed (now in notification settings page)
"""

from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, 
                              QHBoxLayout, QComboBox, QCheckBox,
                              QScrollArea, QWidget, QGroupBox, 
                              QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from theme_manager import ThemeManager
from api_client import APIClient
import json
import os


class SettingsPage(QFrame):
    # Signals for settings changes
    theme_changed = Signal(str)
    pet_changed = Signal(str, str)  # Keep for compatibility
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.settings_file = "settings.json"
        self.user_id = 1
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")
        
        # Create scroll area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background: #424758;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #6c5ce7;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #7d6ee8;
            }
        """)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                color: white;
                font-weight: bold;
                padding-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Appearance Settings
        appearance_group = self.create_group("🎨 Appearance")
        appearance_layout = appearance_group.layout()
        
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Blue", "Purple"])
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #5c6378;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 6px;
                padding: 10px 12px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid white;
                margin-right: 10px;
            }
            QComboBox:hover {
                border: 2px solid #6c5ce7;
            }
            QComboBox QAbstractItemView {
                background-color: #424758;
                color: white;
                selection-background-color: #6c5ce7;
                border: 1px solid #6c748c;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #5c6378;
            }
        """)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)

        # Option: apply theme globally or only to this page
        self.apply_global_check = QCheckBox("Apply theme to entire application")
        self.apply_global_check.setChecked(True)
        self.apply_global_check.setStyleSheet("QCheckBox { color: #cccccc; }")
        appearance_layout.addWidget(self.apply_global_check)
        
        appearance_layout.addWidget(theme_label)
        appearance_layout.addWidget(self.theme_combo)
        layout.addWidget(appearance_group)
        
        # Device Permissions
        permissions_group = self.create_group("🔐 Device Permissions")
        permissions_layout = permissions_group.layout()
        
        perm_desc = QLabel("Manage device access permissions for emotion detection:")
        perm_desc.setStyleSheet("font-size: 13px; color: #b5b8bd; padding-bottom: 5px;")
        permissions_layout.addWidget(perm_desc)
        
        # Microphone
        mic_container = self.create_permission_row(
            "🎤 Microphone Access",
            "Required for voice-based emotion detection"
        )
        self.mic_combo = mic_container.findChild(QComboBox)
        permissions_layout.addWidget(mic_container)
        
        # Camera
        cam_container = self.create_permission_row(
            "📷 Camera Access",
            "Required for facial expression emotion detection"
        )
        self.cam_combo = cam_container.findChild(QComboBox)
        permissions_layout.addWidget(cam_container)
        
        layout.addWidget(permissions_group)
        
        # Notifications Settings
        notif_group = self.create_group("🔔 Notification Preferences")
        notif_layout = notif_group.layout()
        
        notif_desc = QLabel("Configure how you receive emotion notifications:")
        notif_desc.setStyleSheet("font-size: 13px; color: #b5b8bd; padding-bottom: 5px;")
        notif_layout.addWidget(notif_desc)
        
        # Enable notifications checkbox
        notif_container = self.create_checkbox(
            "Enable emotion notifications",
            "Show popup notifications when negative emotions are detected"
        )
        self.notif_check = notif_container.checkbox_widget
        self.notif_check.stateChanged.connect(self.on_notification_toggle)
        
        # Sound checkbox
        sound_container = self.create_checkbox(
            "Enable notification sounds",
            "Play audio alerts with notifications"
        )
        self.sound_check = sound_container.checkbox_widget
        
        # Auto-dismiss checkbox
        auto_dismiss_container = self.create_checkbox(
            "Auto-dismiss notifications",
            "Automatically close notifications after 15 seconds"
        )
        self.auto_dismiss_check = auto_dismiss_container.checkbox_widget
        
        notif_layout.addWidget(notif_container)
        notif_layout.addWidget(sound_container)
        notif_layout.addWidget(auto_dismiss_container)
        
        layout.addWidget(notif_group)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        reset_button = QPushButton("🔄 Reset to Defaults")
        reset_button.clicked.connect(self.reset_to_defaults)
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #5c6378;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6c748c;
            }
        """)
        
        save_button = QPushButton("💾 Save Settings")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 32px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7d6ee8;
            }
            QPushButton:pressed {
                background-color: #5a4cd6;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def create_group(self, title):
        """Create a settings group with title"""
        group = QGroupBox()
        group.setStyleSheet("""
            QGroupBox {
                background-color: #424758;
                border: 1px solid #5c6378;
                border-radius: 12px;
                padding: 20px;
                margin-top: 10px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: white;
                font-weight: bold;
                border: none;
                padding: 0;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title_label)
        
        return group
    
    def create_permission_row(self, title, description):
        """Create a permission setting row"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #5c6378;
                border-radius: 8px;
                padding: 12px;
                margin: 5px 0px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setSpacing(8)
        
        # Title and combo on same row
        top_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: white; font-weight: bold;")
        
        combo = QComboBox()
        combo.addItems(["Always Allow", "Ask Every Time", "Deny"])
        combo.setStyleSheet("""
            QComboBox {
                background-color: #424758;
                color: white;
                border: 1px solid #6c748c;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 1px solid #6c5ce7;
            }
            QComboBox QAbstractItemView {
                background-color: #424758;
                color: white;
                selection-background-color: #6c5ce7;
            }
        """)
        
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(combo)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 12px; color: #b5b8bd;")
        
        layout.addLayout(top_layout)
        layout.addWidget(desc_label)
        
        return container
    
    def create_checkbox(self, text, description):
        """Create a styled checkbox with description"""
        checkbox = QCheckBox(text)
        checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 10px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #6c748c;
                background-color: #5c6378;
            }
            QCheckBox::indicator:checked {
                background-color: #6c5ce7;
                border-color: #6c5ce7;
            }
            QCheckBox::indicator:hover {
                border-color: #7d6ee8;
            }
        """)
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 12px; color: #b5b8bd; padding-left: 30px;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(4)
        layout.addWidget(checkbox)
        layout.addWidget(desc_label)
        
        container.checkbox_widget = checkbox
        
        return container
    
    def load_settings(self):
        """Load settings from file and backend"""
        settings = {}
        
        # Load from local file
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                print("✅ Settings loaded from file")
            except Exception as e:
                print(f"Error loading settings file: {e}")
        
        # Load from backend
        try:
            result = APIClient.get_user_settings(self.user_id)
            if 'error' not in result:
                settings.update(result)
                print("✅ Settings loaded from backend")
        except Exception as e:
            print(f"Error loading from backend: {e}")
        
        # Apply settings to UI
        self.theme_combo.setCurrentText(settings.get('theme', 'Dark'))
        self.mic_combo.setCurrentText(settings.get('mic_permission', 'Always Allow'))
        self.cam_combo.setCurrentText(settings.get('cam_permission', 'Always Allow'))
        self.notif_check.setChecked(settings.get('enable_notifications', True))
        self.sound_check.setChecked(settings.get('sound_notifications', True))
        self.auto_dismiss_check.setChecked(settings.get('auto_dismiss', True))
    
    def on_theme_changed(self, theme_name):
        """Handle theme change immediately"""
        # If user wants global change, use ThemeManager to set app stylesheet
        if getattr(self, 'apply_global_check', None) and self.apply_global_check.isChecked():
            try:
                app = QApplication.instance()
                if app is not None:
                    # Mark app to force clearing local widget styles, then apply
                    setattr(app, '_force_clear_local_styles', True)
                    ThemeManager.apply_theme(app, theme_name)
                    # Remove the temporary flag so future calls don't always clear
                    try:
                        delattr(app, '_force_clear_local_styles')
                    except Exception:
                        pass
                    print(f"🎨 Global theme applied: {theme_name}")
                else:
                    # Fallback to local apply
                    self.apply_theme_local(theme_name)
                    print(f"🎨 Theme preview (local): {theme_name}")
            except Exception as e:
                print(f"Error applying global theme: {e}")
                self.apply_theme_local(theme_name)
        else:
            # Only preview on this page
            self.apply_theme_local(theme_name)
            print(f"🎨 Theme preview (local): {theme_name}")
    
    def on_notification_toggle(self, state):
        """Handle notification enable/disable"""
        enabled = bool(state)
        self.sound_check.setEnabled(enabled)
        self.auto_dismiss_check.setEnabled(enabled)
        
        # Update parent window immediately
        if self.parent_window and hasattr(self.parent_window, 'notifications_enabled'):
            self.parent_window.notifications_enabled = enabled
            print(f"🔔 Notifications {'enabled' if enabled else 'disabled'}")
    
    def save_settings(self):
        """Save all settings to file and backend"""
        try:
            # Collect settings
            settings = {
                'theme': self.theme_combo.currentText(),
                'mic_permission': self.mic_combo.currentText(),
                'cam_permission': self.cam_combo.currentText(),
                'enable_notifications': self.notif_check.isChecked(),
                'sound_notifications': self.sound_check.isChecked(),
                'auto_dismiss': self.auto_dismiss_check.isChecked()
            }
            
            # Save to local file
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print("✅ Settings saved to file")
            
            # Save to backend
            try:
                result = APIClient.update_user_settings(self.user_id, settings)
                
                if 'error' not in result:
                    print("✅ Settings saved to backend")
                    
                    # Update parent window
                    if self.parent_window:
                        if hasattr(self.parent_window, 'notifications_enabled'):
                            self.parent_window.notifications_enabled = settings['enable_notifications']
                        if hasattr(self.parent_window, 'notification_sounds'):
                            self.parent_window.notification_sounds = settings['sound_notifications']
                    
                    # Apply theme
                    self.apply_theme(settings['theme'])
                    
                    QMessageBox.information(self, "✅ Success", 
                        f"Settings saved successfully!\n\n"
                        f"Theme: {settings['theme']}\n"
                        f"Notifications: {'Enabled' if settings['enable_notifications'] else 'Disabled'}\n"
                        f"Microphone: {settings['mic_permission']}\n"
                        f"Camera: {settings['cam_permission']}")
                else:
                    raise Exception(result['error'])
                    
            except Exception as e:
                # Save succeeded locally but not to backend
                QMessageBox.warning(self, "⚠️ Partial Success",
                    f"Settings saved locally, but backend update failed.\n\n"
                    f"Error: {str(e)}\n\n"
                    f"Settings will still work locally.")
                print(f"⚠️ Backend save failed: {e}")
                    
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", 
                f"Failed to save settings:\n{str(e)}")
            print(f"❌ Save settings error: {e}")
    
    def apply_theme(self, theme_name):
        """Apply selected theme"""
        themes = {
            "Dark": {
                "background": "#3a404d",
                "card": "#424758",
                "accent": "#6c5ce7",
                "text": "#ffffff"
            },
            "Light": {
                "background": "#f0f0f0",
                "card": "#ffffff",
                "accent": "#6c5ce7",
                "text": "#2c3e50"
            },
            "Blue": {
                "background": "#2c3e50",
                "card": "#34495e",
                "accent": "#3498db",
                "text": "#ecf0f1"
            },
            "Purple": {
                "background": "#2d1b4e",
                "card": "#3d2b5e",
                "accent": "#9b59b6",
                "text": "#ffffff"
            }
        }
        
        # Backwards-compatible wrapper: respect global checkbox
        if getattr(self, 'apply_global_check', None) and self.apply_global_check.isChecked():
            app = QApplication.instance()
            if app is not None:
                setattr(app, '_force_clear_local_styles', True)
                ThemeManager.apply_theme(app, theme_name)
                try:
                    delattr(app, '_force_clear_local_styles')
                except Exception:
                    pass
                return

        # Otherwise apply theme only to this page
        self.apply_theme_local(theme_name)

    def apply_theme_local(self, theme_name):
        """Apply theme only to this settings page (no global changes)."""
        themes_local = {
            "Dark": {
                "background": "#3a404d",
                "card": "#424758",
                "accent": "#6c5ce7",
                "text": "#ffffff"
            },
            "Light": {
                "background": "#f0f0f0",
                "card": "#ffffff",
                "accent": "#6c5ce7",
                "text": "#2c3e50"
            },
            "Blue": {
                "background": "#2c3e50",
                "card": "#34495e",
                "accent": "#3498db",
                "text": "#ecf0f1"
            },
            "Purple": {
                "background": "#2d1b4e",
                "card": "#3d2b5e",
                "accent": "#9b59b6",
                "text": "#ffffff"
            }
        }

        if theme_name in themes_local:
            th = themes_local[theme_name]
            # Apply only main background for this page and adjust the scroll area/widget style
            self.setStyleSheet(f"background-color: {th['background']};")
            # Update children group boxes/cards by setting a lightweight stylesheet
            for child in self.findChildren(QWidget):
                # Skip top-level main window
                try:
                    child.setStyleSheet("")
                except Exception:
                    pass
            # Keep the detailed widget styles intact; only change this page background
            print(f"🎨 Local theme applied: {theme_name}")
            self.theme_changed.emit(theme_name)
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, 
            "🔄 Reset Settings",
            "Are you sure you want to reset all settings to defaults?\n\n"
            "This will reset:\n"
            "• Theme to Dark\n"
            "• All permissions to Always Allow\n"
            "• Enable all notifications",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.theme_combo.setCurrentText("Dark")
            self.mic_combo.setCurrentText("Always Allow")
            self.cam_combo.setCurrentText("Always Allow")
            self.notif_check.setChecked(True)
            self.sound_check.setChecked(True)
            self.auto_dismiss_check.setChecked(True)
            
            QMessageBox.information(self, "✅ Reset Complete", 
                "Settings have been reset to defaults.\n\n"
                "Click 'Save Settings' to apply changes.")
    
    def update_content(self, pet_name=None):
        """Compatibility method - settings page doesn't use pet name anymore"""
        pass