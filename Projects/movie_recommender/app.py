from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import db, User, Movie, Rating, WatchHistory
from app.tmdb_service import TMDbService
from app.recommendation_engine import RecommendationEngine
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Services
tmdb_service = TMDbService()
recommendation_engine = RecommendationEngine()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes

@app.route('/')
def index():
    """Strona główna z popularnymi filmami"""
    movies_data = tmdb_service.get_popular_movies()
    return render_template('index.html', movies=movies_data['results'] if movies_data else [])


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Rejestracja nowego użytkownika"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Walidacja
        if User.query.filter_by(username=username).first():
            flash('Nazwa użytkownika już istnieje', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email już jest zarejestrowany', 'danger')
            return redirect(url_for('register'))
        
        # Utwórz nowego użytkownika
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Rejestracja zakończona sukcesem! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logowanie użytkownika"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nieprawidłowy email lub hasło', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Wylogowanie użytkownika"""
    logout_user()
    flash('Wylogowano pomyślnie', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Panel użytkownika z rekomendacjami"""
    recommendations = recommendation_engine.get_recommendations(current_user.id)
    
    # Pobierz obiekty filmów
    movie_objects = []
    for rec in recommendations:
        movie = Movie.query.get(rec['movie_id'])
        if movie:
            movie_objects.append(movie)
    
    return render_template('dashboard.html', recommendations=movie_objects)


@app.route('/search')
def search():
    """Wyszukiwanie filmów"""
    query = request.args.get('q', '')
    if query:
        results = tmdb_service.search_movies(query)
        return render_template('search.html', movies=results['results'] if results else [], query=query)
    return render_template('search.html', movies=[], query='')


@app.route('/movie/<int:tmdb_id>')
def movie_detail(tmdb_id):
    """Szczegóły filmu"""
    # Sprawdź czy film jest w bazie
    movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
    
    if not movie:
        # Pobierz z TMDb i dodaj do bazy
        movie_data = tmdb_service.get_movie_details(tmdb_id)
        if movie_data:
            genres = json.dumps([g['name'] for g in movie_data.get('genres', [])])
            movie = Movie(
                tmdb_id=tmdb_id,
                title=movie_data['title'],
                genres=genres,
                release_year=int(movie_data.get('release_date', '0000')[:4]) if movie_data.get('release_date') else None,
                overview=movie_data.get('overview'),
                poster_path=movie_data.get('poster_path'),
                backdrop_path=movie_data.get('backdrop_path'),
                average_rating=movie_data.get('vote_average', 0),
                vote_count=movie_data.get('vote_count', 0),
                popularity=movie_data.get('popularity', 0)
            )
            db.session.add(movie)
            db.session.commit()
    
    # Pobierz ocenę użytkownika jeśli zalogowany
    user_rating = None
    if current_user.is_authenticated:
        rating_obj = Rating.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
        user_rating = rating_obj.rating if rating_obj else None
    
    return render_template('movie_detail.html', movie=movie, user_rating=user_rating)


@app.route('/rate/<int:movie_id>', methods=['POST'])
@login_required
def rate_movie(movie_id):
    """Oceń film"""
    rating_value = float(request.form.get('rating'))
    
    if rating_value < 1 or rating_value > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    # Sprawdź czy ocena już istnieje
    existing_rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    
    if existing_rating:
        existing_rating.rating = rating_value
    else:
        new_rating = Rating(user_id=current_user.id, movie_id=movie_id, rating=rating_value)
        db.session.add(new_rating)
    
    db.session.commit()
    flash('Ocena zapisana!', 'success')
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/my-ratings')
@login_required
def my_ratings():
    """Moje oceny"""
    ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.timestamp.desc()).all()
    return render_template('my_ratings.html', ratings=ratings)


@app.route('/add-to-history/<int:movie_id>', methods=['POST'])
@login_required
def add_to_history(movie_id):
    """Dodaj do historii oglądania"""
    # Sprawdź czy już nie ma w historii
    existing = WatchHistory.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    
    if not existing:
        history = WatchHistory(user_id=current_user.id, movie_id=movie_id)
        db.session.add(history)
        db.session.commit()
        flash('Dodano do historii oglądania', 'success')
    
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/my-history')
@login_required
def my_history():
    """Moja historia oglądania"""
    history = WatchHistory.query.filter_by(user_id=current_user.id).order_by(WatchHistory.watched_at.desc()).all()
    return render_template('my_history.html', history=history)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
