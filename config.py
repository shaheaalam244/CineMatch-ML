"""
Configuration file for Movie Recommendation System
You can use this to separate configuration from main app
"""

import os

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # TMDB API Configuration
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or 'YOUR_TMDB_API_KEY'
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'
    
    # Dataset Configuration
    HOLLYWOOD_DATASET = 'dataset.csv'
    BOLLYWOOD_DATASET = 'bollywood.csv'
    WEBSERIES_DATASET = 'webseries.csv'
    
    # Recommendation Settings
    NUM_RECOMMENDATIONS = 8
    NUM_MOVIES_PER_PAGE = 20
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


# Default configuration
config = DevelopmentConfig()


# Usage in app.py:
# from config import config
# app.config.from_object(config)
# TMDB_API_KEY = config.TMDB_API_KEY