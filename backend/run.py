#!/usr/bin/env python3
"""
Startup script for MoodMate Backend
This script sets up the environment and starts the Flask application
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ Created data directory: {data_dir}")
    else:
        print(f"✅ Data directory exists: {data_dir}")

def start_backend():
    """Start the Flask backend"""
    print("\n🚀 Starting MoodMate Backend...")
    print("=" * 50)
    
    try:
        # MODIFIED: Import the factory function and init function
        from app import create_app, init_default_data
        
        # MODIFIED: Call the factory to create the app instance
        app = create_app()

        # Initialize default data
        init_default_data()
        
        print("✅ Backend initialized successfully")
        print("🌐 Backend will be available at: http://127.0.0.1:5000/api")
        print("🩺 Health check endpoint: http://127.0.0.1:5000/api/health")
        print("⏹️  Press Ctrl+C to stop the backend")
        print("=" * 50)
        
        # Start the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all requirements are installed")
        return False
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def main():
    """Main startup function"""
    print("🎭 MoodMate Backend Startup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create data directory
    create_data_directory()
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Backend stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the error message above and try again")

