from flask import Flask, jsonify
from flask_cors import CORS
from .routes import main_bp

__all__ = ['main_bp']

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable Cross-Origin Resource Sharing to allow the frontend to make requests
    CORS(app)

    # Register the blueprint that contains our API routes
    app.register_blueprint(main_bp)

    @app.route('/')
    def index():
        # This is the response that will be sent
        return jsonify({"status": "success", "message": "Welcome to the Moodmate API!"})

    return app
