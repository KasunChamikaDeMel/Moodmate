"""
Global Theme Manager for MoodMate
Place this in: frontend/theme_manager.py
"""

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class ThemeManager:
    """Manage application-wide themes"""
    
    THEMES = {
        "Dark": {
            "background": "#3a404d",
            "card": "#424758",
            "card_hover": "#4a5263",
            "secondary": "#5c6378",
            "accent": "#6c5ce7",
            "accent_hover": "#7d6ee8",
            "text": "#ffffff",
            "text_secondary": "#cccccc",
            "text_muted": "#95a5a6",
            "border": "#6c748c",
            "success": "#27ae60",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        },
        "Light": {
            "background": "#f0f0f0",
            "card": "#ffffff",
            "card_hover": "#f8f9fa",
            "secondary": "#e9ecef",
            "accent": "#6c5ce7",
            "accent_hover": "#7d6ee8",
            "text": "#2c3e50",
            "text_secondary": "#34495e",
            "text_muted": "#7f8c8d",
            "border": "#dee2e6",
            "success": "#27ae60",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        },
        "Blue": {
            "background": "#2c3e50",
            "card": "#34495e",
            "card_hover": "#3d566e",
            "secondary": "#4a6278",
            "accent": "#3498db",
            "accent_hover": "#5dade2",
            "text": "#ecf0f1",
            "text_secondary": "#bdc3c7",
            "text_muted": "#95a5a6",
            "border": "#4a6278",
            "success": "#2ecc71",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        },
        "Purple": {
            "background": "#2d1b4e",
            "card": "#3d2b5e",
            "card_hover": "#4d3b6e",
            "secondary": "#5d4b7e",
            "accent": "#9b59b6",
            "accent_hover": "#b370cf",
            "text": "#ffffff",
            "text_secondary": "#e0d5f5",
            "text_muted": "#b19cd9",
            "border": "#6d5b8e",
            "success": "#27ae60",
            "warning": "#f39c12",
            "danger": "#e74c3c"
        }
    }
    
    current_theme = "Dark"
    
    @staticmethod
    def get_stylesheet(theme_name="Dark"):
        """Get complete application stylesheet"""
        theme = ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES["Dark"])
        
        return f"""
            /* Global Styles */
            QMainWindow, QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
            }}
            
            /* Frames and Cards */
            QFrame {{
                background-color: {theme['card']};
                border-radius: 10px;
            }}
            
            QGroupBox {{
                background-color: {theme['card']};
                border: 1px solid {theme['border']};
                border-radius: 12px;
                padding: 20px;
                margin-top: 10px;
                color: {theme['text']};
                font-weight: bold;
            }}
            
            /* Labels */
            QLabel {{
                color: {theme['text']};
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {theme['accent']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {theme['accent_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {theme['accent']};
            }}
            
            QPushButton:disabled {{
                background-color: {theme['secondary']};
                color: {theme['text_muted']};
            }}
            
            /* Input Fields */
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {theme['secondary']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 2px solid {theme['accent']};
            }}
            
            /* ComboBox */
            QComboBox {{
                background-color: {theme['secondary']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            
            QComboBox:hover {{
                border: 2px solid {theme['accent']};
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {theme['card']};
                color: {theme['text']};
                selection-background-color: {theme['accent']};
                border: 1px solid {theme['border']};
            }}
            
            /* Checkboxes */
            QCheckBox {{
                color: {theme['text']};
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {theme['border']};
                background-color: {theme['secondary']};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {theme['accent']};
                border-color: {theme['accent']};
            }}
            
            /* Radio Buttons */
            QRadioButton {{
                color: {theme['text']};
                spacing: 8px;
            }}
            
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {theme['border']};
                background-color: {theme['secondary']};
            }}
            
            QRadioButton::indicator:checked {{
                background-color: {theme['accent']};
                border-color: {theme['accent']};
            }}
            
            /* Lists */
            QListWidget {{
                background-color: {theme['card']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 10px;
            }}
            
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {theme['border']};
            }}
            
            QListWidget::item:selected {{
                background-color: {theme['accent']};
            }}
            
            QListWidget::item:hover {{
                background-color: {theme['card_hover']};
            }}
            
            /* Scroll Areas */
            QScrollArea {{
                border: none;
                background-color: {theme['background']};
            }}
            
            QScrollBar:vertical {{
                background: {theme['card']};
                width: 10px;
                border-radius: 5px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {theme['accent']};
                min-height: 30px;
                border-radius: 5px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: {theme['accent_hover']};
            }}
            
            /* Sliders */
            QSlider::groove:horizontal {{
                border: 1px solid {theme['border']};
                height: 8px;
                background: {theme['secondary']};
                border-radius: 4px;
            }}
            
            QSlider::handle:horizontal {{
                background: {theme['accent']};
                border: 2px solid {theme['accent_hover']};
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
        """
    
    @staticmethod
    def apply_theme(app, theme_name="Dark"):
        """Apply theme to entire application"""
        ThemeManager.current_theme = theme_name
        stylesheet = ThemeManager.get_stylesheet(theme_name)

        # Clear locally-applied widget styles if requested via keyword
        # If caller passes force_clear_local=True, remove per-widget styles
        # so the application stylesheet can take full effect.
        force_clear = False
        try:
            # Expect optional attribute set on app for backward compatibility
            force_clear = getattr(app, '_force_clear_local_styles', False)
        except Exception:
            force_clear = False

        if force_clear:
            try:
                for top in app.topLevelWidgets():
                    try:
                        top.setStyleSheet("")
                    except Exception:
                        pass
                    # Clear children styles
                    for child in top.findChildren(QWidget):
                        try:
                            child.setStyleSheet("")
                        except Exception:
                            pass
            except Exception:
                pass

        app.setStyleSheet(stylesheet)
        print(f"✅ Theme applied: {theme_name} (force_clear_local={force_clear})")
    
    @staticmethod
    def get_color(color_key, theme_name=None):
        """Get specific color from theme"""
        if theme_name is None:
            theme_name = ThemeManager.current_theme
        theme = ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES["Dark"])
        return theme.get(color_key, "#ffffff")