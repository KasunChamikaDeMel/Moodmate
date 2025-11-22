#!/usr/bin/env python3
"""
Startup script for MoodMate Backend
This script sets up the environment and starts the Flask application
"""

import os
import sys
import subprocess
import time
import platform
import threading
import requests

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

def check_pet_app_running():
    """Check if pet app is running by testing ports"""
    ports_to_try = [4000, 4001, 4002, 4003, 4004, 4005]
    for port in ports_to_try:
        try:
            response = requests.get(f"http://localhost:{port}/trigger", timeout=0.2)
            return True, port
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            continue
        except:
            return True, port
    return False, None

def start_pet_app():
    """Start the Electron pet app in background"""
    is_running, port = check_pet_app_running()
    if is_running:
        print(f"🐾 Pet app is already running on port {port}")
        return
    
    try:
        # Get the project root directory (go up from backend/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        pet_dir = os.path.join(project_root, 'moodmate-pet')
        
        if not os.path.exists(pet_dir):
            print(f"⚠️ Pet app directory not found: {pet_dir}")
            return
        
        # Check if node_modules exists (dependencies installed)
        node_modules = os.path.join(pet_dir, 'node_modules')
        if not os.path.exists(node_modules):
            print("⚠️ Pet app dependencies not installed. Please run 'npm install' in moodmate-pet directory")
            return
        
        # Start Electron app in background (show CMD window for startup messages, then minimize)
        if platform.system() == 'Windows':
            # Use 'start /MIN' to start minimized, so user can see it started but it doesn't block
            subprocess.Popen(
                ['cmd', '/c', 'start', '/MIN', 'cmd', '/k', 'npm', 'start'],
                cwd=pet_dir,
                shell=False
            )
        else:
            subprocess.Popen(
                ['npm', 'start'],
                cwd=pet_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        
        print("🚀 Starting Electron pet app in background...")
        
        # Check if it started successfully (with retries)
        for i in range(10):
            time.sleep(0.5)
            is_running, port = check_pet_app_running()
            if is_running:
                print(f"✅ Pet app started successfully on port {port}")
                return
        
        print("⚠️ Pet app may still be starting. It will be ready when needed.")
                
    except Exception as e:
        print(f"❌ Error starting pet app: {e}")

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
    
    # Start pet app in background thread (before backend) - only if not already running
    print("\n🐾 Checking Pet App...")
    is_running, port = check_pet_app_running()
    if not is_running:
        print("🚀 Starting Pet App...")
        pet_thread = threading.Thread(target=start_pet_app, daemon=True)
        pet_thread.start()
        time.sleep(3)  # Give pet app a moment to start
    else:
        print(f"✅ Pet App already running on port {port}")
    
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

