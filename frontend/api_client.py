import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class APIClient:
    """Centralized API client for frontend-backend communication"""
    
    BASE_URL = "http://localhost:5000/api"
    TIMEOUT = 10
    
    @staticmethod
    def _handle_response(response):
        """Handle API response and errors"""
        try:
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                return {"error": "Invalid credentials"}
            elif response.status_code == 400:
                return {"error": response.json().get('error', 'Bad request')}
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
    
    # ==================== AUTHENTICATION ====================
    
    @staticmethod
    def register(username: str, email: str, password_hash: str) -> Dict:
        """Register new user"""
        return APIClient._make_request("POST", "/auth/register", {
            "username": username,
            "email": email,
            "password": password_hash
        })
    
    @staticmethod
    def login(email: str, password_hash: str) -> Dict:
        """User login"""
        return APIClient._make_request("POST", "/auth/login", {
            "email": email,
            "password": password_hash
        })
    
    # ==================== USER MANAGEMENT ====================
    
    @staticmethod
    def get_user(user_id: int = 1) -> Dict:
        """Get user information"""
        return APIClient._make_request("GET", f"/user/{user_id}")
    
    @staticmethod
    def update_user(user_id: int, data: Dict) -> Dict:
        """Update user profile"""
        return APIClient._make_request("PUT", f"/user/{user_id}", data)
    
    # ==================== USER SETTINGS ====================
    
    @staticmethod
    def get_user_settings(user_id: int) -> Dict:
        """Get user settings from backend"""
        result = APIClient._make_request("GET", f"/users/{user_id}/settings")
        if 'error' in result:
            # Return defaults if error
            return {
                'theme': 'Dark',
                'mic_permission': 'Always Allow',
                'cam_permission': 'Always Allow',
                'enable_notifications': True,
                'sound_notifications': True,
                'auto_dismiss': True
            }
        return result
    
    @staticmethod
    def update_user_settings(user_id: int, settings: Dict) -> Dict:
        """Update user settings in backend"""
        return APIClient._make_request("PUT", f"/users/{user_id}/settings", settings)
    
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
            return []
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


# Test function
def test_api_client():
    """Test API client functionality"""
    print("Testing API Client...")
    print(f"Backend URL: {APIClient.BASE_URL}")
    
    # Test connection
    if APIClient.test_connection():
        print("✅ Backend connection successful!")
    else:
        print("❌ Backend connection failed!")
        return
    
    print("\n✅ API Client test complete!")


if __name__ == "__main__":
    test_api_client()