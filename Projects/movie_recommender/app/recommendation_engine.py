import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Movie, Rating, User
from config import Config
import json

class RecommendationEngine:
    def __init__(self):
        self.content_weight = Config.CONTENT_BASED_WEIGHT
        self.collaborative_weight = Config.COLLABORATIVE_WEIGHT
        self.min_ratings = Config.MIN_RATINGS_FOR_COLLABORATIVE
        self.top_n = Config.TOP_N_RECOMMENDATIONS
    
    def get_recommendations(self, user_id):
        """
        Główna metoda - zwraca hybrydowe rekomendacje dla użytkownika
        """
        content_scores = self._content_based_filtering(user_id)
        collaborative_scores = self._collaborative_filtering(user_id)
        
        # Kombinacja wyników
        if collaborative_scores is not None and len(collaborative_scores) > 0:
            # Użyj obu metod
            hybrid_scores = self._combine_scores(content_scores, collaborative_scores)
        else:
            # Tylko content-based dla nowych użytkowników
            hybrid_scores = content_scores
        
        return hybrid_scores[:self.top_n]
    
    def _content_based_filtering(self, user_id):
        """
        Content-Based Filtering: rekomendacje na podstawie gatunków filmów
        """
        # Pobierz oceny użytkownika
        user_ratings = Rating.query.filter_by(user_id=user_id).all()
        
        if not user_ratings:
            # Zwróć popularne filmy dla nowych użytkowników
            return self._get_popular_movies()
        
        # Pobierz filmy które użytkownik ocenił pozytywnie (>= 3.5)
        liked_movie_ids = [r.movie_id for r in user_ratings if r.rating >= 3.5]
        
        if not liked_movie_ids:
            return self._get_popular_movies()
        
        # Pobierz wszystkie filmy z bazy
        all_movies = Movie.query.all()
        
        # Stwórz macierz cech (genres jako tekst)
        movies_data = []
        for movie in all_movies:
            genres_str = ' '.join(json.loads(movie.genres)) if movie.genres else ''
            movies_data.append({
                'id': movie.id,
                'genres': genres_str,
                'title': movie.title
            })
        
        df = pd.DataFrame(movies_data)
        
        # TF-IDF vectorization
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['genres'])
        
        # Oblicz podobieństwo
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Znajdź podobne filmy do tych które użytkownik lubi
        similar_movies = []
        for movie_id in liked_movie_ids:
            idx = df[df['id'] == movie_id].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            for i, score in sim_scores[1:31]:  # Top 30 podobnych
                movie_id_candidate = df.iloc[i]['id']
                # Nie rekomenduj filmów już ocenionych
                if movie_id_candidate not in [r.movie_id for r in user_ratings]:
                    similar_movies.append({
                        'movie_id': movie_id_candidate,
                        'score': score
                    })
        
        # Agreguj wyniki i posortuj
        movie_scores = {}
        for item in similar_movies:
            mid = item['movie_id']
            if mid not in movie_scores:
                movie_scores[mid] = []
            movie_scores[mid].append(item['score'])
        
        # Średni score dla każdego filmu
        recommendations = [
            {'movie_id': mid, 'score': np.mean(scores)}
            for mid, scores in movie_scores.items()
        ]
        recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
        
        return recommendations
    
    def _collaborative_filtering(self, user_id):
        """
        Collaborative Filtering: rekomendacje na podstawie podobnych użytkowników
        """
        # Pobierz wszystkie oceny
        all_ratings = Rating.query.all()
        
        if len(all_ratings) < self.min_ratings:
            return None
        
        # Stwórz macierz user-movie
        ratings_data = [
            {'user_id': r.user_id, 'movie_id': r.movie_id, 'rating': r.rating}
            for r in all_ratings
        ]
        df = pd.DataFrame(ratings_data)
        
        # User-movie matrix
        user_movie_matrix = df.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating'
        ).fillna(0)
        
        # Oblicz podobieństwo między użytkownikami (Cosine Similarity)
        user_similarity = cosine_similarity(user_movie_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity,
            index=user_movie_matrix.index,
            columns=user_movie_matrix.index
        )
        
        # Znajdź podobnych użytkowników
        if user_id not in user_similarity_df.index:
            return None
        
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:11]  # Top 10 podobnych
        
        # Znajdź filmy ocenione przez podobnych użytkowników
        recommendations = {}
        user_rated_movies = set(df[df['user_id'] == user_id]['movie_id'])
        
        for similar_user_id, similarity_score in similar_users.items():
            similar_user_ratings = df[df['user_id'] == similar_user_id]
            
            for _, row in similar_user_ratings.iterrows():
                movie_id = row['movie_id']
                rating = row['rating']
                
                # Nie rekomenduj filmów już ocenionych
                if movie_id not in user_rated_movies and rating >= 3.5:
                    if movie_id not in recommendations:
                        recommendations[movie_id] = []
                    # Ważona ocena według podobieństwa użytkowników
                    recommendations[movie_id].append(rating * similarity_score)
        
        # Oblicz średnią ważoną dla każdego filmu
        result = [
            {'movie_id': mid, 'score': np.mean(scores)}
            for mid, scores in recommendations.items()
        ]
        result = sorted(result, key=lambda x: x['score'], reverse=True)
        
        return result
    
    def _combine_scores(self, content_scores, collaborative_scores):
        """
        Łączy wyniki z obu metod używając wag
        """
        combined = {}
        
        # Content-based scores
        for item in content_scores:
            mid = item['movie_id']
            combined[mid] = item['score'] * self.content_weight
        
        # Collaborative scores
        for item in collaborative_scores:
            mid = item['movie_id']
            if mid in combined:
                combined[mid] += item['score'] * self.collaborative_weight
            else:
                combined[mid] = item['score'] * self.collaborative_weight
        
        result = [
            {'movie_id': mid, 'score': score}
            for mid, score in combined.items()
        ]
        result = sorted(result, key=lambda x: x['score'], reverse=True)
        
        return result
    
    def _get_popular_movies(self):
        """
        Zwraca popularne filmy (dla cold start)
        """
        popular = Movie.query.order_by(Movie.popularity.desc()).limit(50).all()
        return [{'movie_id': m.id, 'score': m.popularity} for m in popular]
