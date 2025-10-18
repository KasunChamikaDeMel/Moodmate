#!/usr/bin/env python3
"""
Test script for MoodMate Backend API
Run this after starting the backend to test all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:5000")
        return False
    return True

def test_user_profile():
    """Test user profile endpoints"""
    print("\nTesting user profile...")
    
    # Get profile
    response = requests.get(f"{BASE_URL}/api/user/profile")
    if response.status_code == 200:
        print("✅ Get profile passed")
        user_data = response.json()
        print(f"   Current user: {user_data.get('username', 'Unknown')}")
    else:
        print(f"❌ Get profile failed: {response.status_code}")
        return False
    
    # Update profile
    update_data = {"username": "TestUser", "email": "test@example.com"}
    response = requests.put(f"{BASE_URL}/api/user/profile", json=update_data)
    if response.status_code == 200:
        print("✅ Update profile passed")
        updated_user = response.json()
        print(f"   Updated username: {updated_user.get('username')}")
    else:
        print(f"❌ Update profile failed: {response.status_code}")
        return False
    
    return True

def test_pet_management():
    """Test pet management endpoints"""
    print("\nTesting pet management...")
    
    # Get pet info
    response = requests.get(f"{BASE_URL}/api/pet/info")
    if response.status_code == 200:
        print("✅ Get pet info passed")
        pet_data = response.json()
        print(f"   Pet name: {pet_data.get('pet_name')}, Mood: {pet_data.get('pet_mood')}")
    else:
        print(f"❌ Get pet info failed: {response.status_code}")
        return False
    
    # Feed pet
    response = requests.post(f"{BASE_URL}/api/pet/feed")
    if response.status_code == 200:
        print("✅ Feed pet passed")
        updated_pet = response.json()
        print(f"   New mood: {updated_pet.get('pet_mood')}, Exp: {updated_pet.get('pet_exp')}")
    else:
        print(f"❌ Feed pet failed: {response.status_code}")
        return False
    
    # Play with pet
    response = requests.post(f"{BASE_URL}/api/pet/play")
    if response.status_code == 200:
        print("✅ Play with pet passed")
        updated_pet = response.json()
        print(f"   New mood: {updated_pet.get('pet_mood')}, Exp: {updated_pet.get('pet_exp')}")
    else:
        print(f"❌ Play with pet failed: {response.status_code}")
        return False
    
    return True

def test_mood_tracking():
    """Test mood tracking endpoints"""
    print("\nTesting mood tracking...")
    
    # Get current mood
    response = requests.get(f"{BASE_URL}/api/mood/current")
    if response.status_code == 200:
        print("✅ Get current mood passed")
        mood_data = response.json()
        print(f"   Current mood: {mood_data.get('current_mood')}")
    else:
        print(f"❌ Get current mood failed: {response.status_code}")
        return False
    
    # Add mood detection
    detection_data = {
        "detected_mood": "happy",
        "confidence": 0.85,
        "notes": "Feeling great today!"
    }
    response = requests.post(f"{BASE_URL}/api/mood/detect", json=detection_data)
    if response.status_code == 200:
        print("✅ Mood detection passed")
        result = response.json()
        print(f"   Detected mood: {result.get('detected_mood')}, Confidence: {result.get('confidence')}")
    else:
        print(f"❌ Mood detection failed: {response.status_code}")
        return False
    
    # Add manual mood entry
    manual_mood = {
        "mood": "excited",
        "notes": "Manual entry test"
    }
    response = requests.post(f"{BASE_URL}/api/mood/history", json=manual_mood)
    if response.status_code == 200:
        print("✅ Manual mood entry passed")
        entry = response.json()
        print(f"   Added mood: {entry.get('mood')}")
    else:
        print(f"❌ Manual mood entry failed: {response.status_code}")
        return False
    
    # Get mood history
    response = requests.get(f"{BASE_URL}/api/mood/history")
    if response.status_code == 200:
        print("✅ Get mood history passed")
        history = response.json()
        print(f"   Total entries: {len(history.get('mood_history', []))}")
    else:
        print(f"❌ Get mood history failed: {response.status_code}")
        return False
    
    return True

def test_settings():
    """Test settings endpoints"""
    print("\nTesting settings...")
    
    # Get settings
    response = requests.get(f"{BASE_URL}/api/settings")
    if response.status_code == 200:
        print("✅ Get settings passed")
        settings = response.json()
        print(f"   Theme: {settings.get('theme')}, Notifications: {settings.get('notifications_enabled')}")
    else:
        print(f"❌ Get settings failed: {response.status_code}")
        return False
    
    # Update settings
    new_settings = {"theme": "dark", "notifications_enabled": False}
    response = requests.put(f"{BASE_URL}/api/settings", json=new_settings)
    if response.status_code == 200:
        print("✅ Update settings passed")
        result = response.json()
        print(f"   Update result: {result.get('success')}")
    else:
        print(f"❌ Update settings failed: {response.status_code}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 MoodMate Backend API Test Suite")
    print("=" * 40)
    
    # Check if backend is running
    if not test_health_check():
        print("\n❌ Backend is not running. Please start it first with: python app.py")
        return
    
    tests = [
        test_user_profile,
        test_pet_management,
        test_mood_tracking,
        test_settings
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
