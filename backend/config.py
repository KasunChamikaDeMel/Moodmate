import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kasun'