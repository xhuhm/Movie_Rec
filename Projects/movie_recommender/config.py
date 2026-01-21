import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # TMDb API
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    TMDB_BASE_URL = os.environ.get('TMDB_BASE_URL') or 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
    
    # Recommendation settings
    MIN_RATINGS_FOR_COLLABORATIVE = 5  # Minimum ratings before using collaborative filtering
    CONTENT_BASED_WEIGHT = 0.7
    COLLABORATIVE_WEIGHT = 0.3
    TOP_N_RECOMMENDATIONS = 10
