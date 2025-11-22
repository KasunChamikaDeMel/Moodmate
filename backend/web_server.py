import http.server
import socketserver
import os
import threading

PORT = 8000
# Calculate the absolute path to the 'moodmate-pet' directory
# It is located at the project root, which is one level up from 'backend/web_server.py'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DIRECTORY = os.path.join(PROJECT_ROOT, "moodmate-pet")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Pass the absolute path to the directory argument
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    # Removed os.chdir here as it caused issues with Flask reloader

    # Ensure the directory exists before starting the server
    if not os.path.isdir(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found. Cannot start web server.")
        return

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving moodmate-pet at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # This block is for testing the server independently
    # In the actual app, it will be started as a thread
    start_server()
