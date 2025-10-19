"""
API Client for MoodMate Frontend
Handles all communication with the Flask backend
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class APIClient:
    """Centralized API client for frontend-backend communication"""
    
    BASE_URL = "http://localhost:5000/api"
    TIMEOUT = 10  # seconds
    
    @staticmethod
    def _handle_response(response):
        """Handle API response and errors"""
        try:
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response from server"}
        except Exception as e:
            return {"error": f"Response handling error: {str(e)}"}
    
    @staticmethod
    def _make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to backend"""
        url = f"{APIClient.BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=APIClient.TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=APIClient.TIMEOUT)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=APIClient.TIMEOUT)
            elif method == "DELETE":
                response = requests.delete(url, timeout=APIClient.TIMEOUT)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}
            
            return APIClient._handle_response(response)
            
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to backend. Is the server running?"}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    # ==================== USER MANAGEMENT ====================
    
    @staticmethod
    def get_user(user_id: int = 1) -> Dict:
        """Get user information"""
        return APIClient._make_request("GET", f"/user/{user_id}")
    
    @staticmethod
    def update_user(user_id: int, data: Dict) -> Dict:
        """Update user profile"""
        return APIClient._make_request("PUT", f"/user/{user_id}", data)
    
    @staticmethod
    def login(username: str, password: str) -> Dict:
        """User login (placeholder for future authentication)"""
        return APIClient._make_request("POST", "/auth/login", {
            "username": username,
            "password": password
        })
    
    # ==================== EMOTION DETECTION ====================
    
    @staticmethod
    def predict_face_emotion(image_base64: str) -> Dict:
        """Send face image for emotion detection"""
        return APIClient._make_request("POST", "/predict_face", {
            "image": image_base64
        })
    
    @staticmethod
    def predict_voice_emotion(audio_base64: str) -> Dict:
        """Send audio for emotion detection"""
        return APIClient._make_request("POST", "/predict_voice", {
            "audio": audio_base64
        })
    
    @staticmethod
    def predict_text_emotion(text: str) -> Dict:
        """Send text for emotion analysis"""
        return APIClient._make_request("POST", "/predict_text", {
            "text": text
        })
    
    # ==================== MOOD HISTORY ====================
    
    @staticmethod
    def get_mood_history(user_id: int = 1) -> List[Dict]:
        """Get mood history for a user"""
        result = APIClient._make_request("GET", f"/mood_history/{user_id}")
        if isinstance(result, dict) and 'error' in result:
            return result
        return result if isinstance(result, list) else []
    
    @staticmethod
    def add_mood_entry(user_id: int, mood: str, source: str = "manual") -> Dict:
        """Add a new mood entry"""
        return APIClient._make_request("POST", "/mood_history", {
            "user_id": user_id,
            "mood": mood,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    def delete_mood_entry(entry_id: int) -> Dict:
        """Delete a mood history entry"""
        return APIClient._make_request("DELETE", f"/mood_history/{entry_id}")
    
    # ==================== PET MANAGEMENT ====================
    
    @staticmethod
    def get_pet_data(user_id: int = 1) -> Dict:
        """Get pet data for a user"""
        return APIClient._make_request("GET", f"/pet/{user_id}")
    
    @staticmethod
    def update_pet_data(user_id: int, data: Dict) -> Dict:
        """Update pet information"""
        return APIClient._make_request("PUT", f"/pet/{user_id}", data)
    
    @staticmethod
    def feed_pet(user_id: int) -> Dict:
        """Feed the pet"""
        return APIClient._make_request("POST", f"/pet/{user_id}/feed")
    
    @staticmethod
    def update_pet_mood(user_id: int, mood: str) -> Dict:
        """Update pet's mood based on user emotion"""
        return APIClient._make_request("PUT", f"/pet/{user_id}/mood", {
            "mood": mood
        })
    
    # ==================== HEALTH CHECK ====================
    
    @staticmethod
    def health_check() -> Dict:
        """Check if backend is running"""
        return APIClient._make_request("GET", "/health")
    
    @staticmethod
    def test_connection() -> bool:
        """Test if backend is reachable"""
        result = APIClient.health_check()
        return not ('error' in result)