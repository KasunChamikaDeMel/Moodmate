from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox
import sys
import traceback

from sidebar import MoodMateApp


def global_exception_handler(exc_type, exc_value, exc_tb):
    """Global exception handler to prevent silent crashes"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f"[CRASH] Unhandled exception:\n{error_msg}")
    
    # Try to show a message box if app is running
    try:
        app = QApplication.instance()
        if app:
            QMessageBox.critical(None, "MoodMate Error", 
                f"An unexpected error occurred:\n\n{exc_value}\n\n"
                "The application will continue running.\n"
                "Check console for details.")
    except Exception:
        pass


# Install global exception handler
sys.excepthook = global_exception_handler


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    try:
        window = MoodMateApp()
        window.show()
        return app.exec()
    except Exception as e:
        print(f"[CRASH] Failed to start application: {e}")
        traceback.print_exc()
        QMessageBox.critical(None, "Startup Error", 
            f"Failed to start MoodMate:\n\n{e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
else:
    # Legacy compatibility: direct execution without __main__ guard
    app = QApplication(sys.argv)
    window = MoodMateApp()
    window.show()
    app.exec()
