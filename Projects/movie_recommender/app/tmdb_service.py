import requests
import json
from config import Config

class TMDbService:
    def __init__(self):
        self.api_key = Config.TMDB_API_KEY
        self.base_url = Config.TMDB_BASE_URL
        self.image_base_url = Config.TMDB_IMAGE_BASE_URL
    
    def get_popular_movies(self, page=1):
        """Pobiera popularne filmy z TMDb"""
        url = f"{self.base_url}/movie/popular"
        params = {
            'api_key': self.api_key,
            'language': 'pl-PL',
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def search_movies(self, query, page=1):
        """Wyszukuje filmy po tytule"""
        url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'language': 'pl-PL',
            'query': query,
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_movie_details(self, tmdb_id):
        """Pobiera szczegóły filmu"""
        url = f"{self.base_url}/movie/{tmdb_id}"
        params = {
            'api_key': self.api_key,
            'language': 'pl-PL'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_movie_genres(self):
        """Pobiera listę wszystkich gatunków"""
        url = f"{self.base_url}/genre/movie/list"
        params = {
            'api_key': self.api_key,
            'language': 'pl-PL'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['genres']
        return []
    
    def discover_by_genre(self, genre_id, page=1):
        """Wyszukuje filmy po gatunku"""
        url = f"{self.base_url}/discover/movie"
        params = {
            'api_key': self.api_key,
            'language': 'pl-PL',
            'with_genres': genre_id,
            'page': page,
            'sort_by': 'popularity.desc'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_poster_url(self, poster_path):
        """Zwraca pełny URL do plakatu filmu"""
        if poster_path:
            return f"{self.image_base_url}{poster_path}"
        return None
