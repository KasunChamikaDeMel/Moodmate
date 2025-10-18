# MoodMate Backend

A Flask-based backend API for the MoodMate emotional companion application.

## Features

- **User Management**: Profile creation and updates
- **Pet System**: Virtual pet interaction (feed, play, mood tracking)
- **Mood Detection**: API endpoints for mood tracking and history
- **Settings Management**: Application configuration
- **RESTful API**: Clean, documented endpoints
- **CORS Support**: Frontend integration ready

## API Endpoints

### Health Check
- `GET /api/health` - Backend status check

### User Profile
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

### Pet Management
- `GET /api/pet/info` - Get pet information
- `POST /api/pet/feed` - Feed the pet
- `POST /api/pet/play` - Play with the pet

### Mood Tracking
- `GET /api/mood/current` - Get current mood
- `POST /api/mood/detect` - Process mood detection
- `GET /api/mood/history` - Get mood history
- `POST /api/mood/history` - Add manual mood entry

### Settings
- `GET /api/settings` - Get application settings
- `PUT /api/settings` - Update application settings

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Backend
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### 3. Test the API
```bash
curl http://localhost:5000/api/health
```

## Data Storage

The backend uses JSON files for data storage (suitable for development):
- `data/users.json` - User profiles
- `data/pet_data.json` - Pet information
- `data/mood_history.json` - Mood tracking history

## Environment Variables

- `FLASK_ENV` - Set to 'development', 'production', or 'testing'
- `SECRET_KEY` - Secret key for production (optional in development)

## Frontend Integration

The backend is designed to work with your existing PySide6 frontend. You can:

1. **Replace local data storage** with API calls
2. **Add real-time updates** using periodic API polling
3. **Implement user authentication** (future enhancement)
4. **Add database support** for production deployment

## Example Frontend Integration

```python
import requests

# Get current mood
response = requests.get('http://localhost:5000/api/mood/current')
current_mood = response.json()['current_mood']

# Update pet mood
response = requests.post('http://localhost:5000/api/pet/feed')
pet_data = response.json()
```

## Development

### Adding New Endpoints
1. Add route in `app.py`
2. Update this README
3. Test with frontend integration

### Database Migration
For production, consider migrating from JSON files to:
- SQLite (simple)
- PostgreSQL (robust)
- MongoDB (flexible)

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set proper `SECRET_KEY`
4. Use environment variables for configuration
5. Implement proper authentication and authorization

## Troubleshooting

### Common Issues
- **Port already in use**: Change port in `app.py`
- **CORS errors**: Check CORS configuration in `config.py`
- **Data not saving**: Ensure `data/` directory exists and is writable

### Logs
Check console output for error messages and API requests.

## Future Enhancements

- User authentication and authorization
- Real-time notifications (WebSocket)
- Machine learning integration for mood detection
- Database support
- API rate limiting
- Comprehensive testing suite
