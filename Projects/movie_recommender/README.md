# MovieRec - System Rekomendacji Filmów oparty na AI

System rekomendacji filmów wykorzystujący hybrydowe algorytmy sztucznej inteligencji do personalizacji sugestii filmowych.

## 📋 Opis projektu

MovieRec to aplikacja webowa, która rekomenduje filmy użytkownikom na podstawie ich preferencji, historii oglądania i ocen. System wykorzystuje zaawansowane algorytmy uczenia maszynowego:

- **Content-Based Filtering** - rekomendacje na podstawie cech filmów (gatunki, rok produkcji)
- **Collaborative Filtering** - rekomendacje na podstawie podobnych użytkowników
- **Hybrid Approach** - kombinacja obu metod dla lepszej dokładności

## 🚀 Funkcjonalności

- ✅ Rejestracja i logowanie użytkowników
- ✅ Przeglądanie i wyszukiwanie filmów
- ✅ System oceniania filmów (1-5 gwiazdek)
- ✅ Historia oglądania
- ✅ Personalizowane rekomendacje AI
- ✅ Responsywny interfejs (Bootstrap 5)
- ✅ Integracja z TMDb API

## 🛠️ Technologie

### Backend
- Python 3.10+
- Flask 3.0
- SQLAlchemy (ORM)
- Flask-Login (autoryzacja)

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Font Awesome

### AI/ML
- pandas, numpy
- scikit-learn (TF-IDF, Cosine Similarity)
- TMDb API

### Baza danych
- SQLite

## 📦 Instalacja

### 1. Klonowanie repozytorium

```bash
git clone <repository_url>
cd movie_recommender
```

### 2. Utworzenie środowiska wirtualnego

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Konfiguracja TMDb API

1. Zarejestruj się na [TMDb](https://www.themoviedb.org/)
2. Uzyskaj klucz API w [Settings > API](https://www.themoviedb.org/settings/api)
3. Skopiuj `.env.example` do `.env`
4. Dodaj swój klucz API do pliku `.env`:

```bash
TMDB_API_KEY=twoj_klucz_api_tutaj
SECRET_KEY=losowy_sekretny_klucz
```

### 5. Inicjalizacja bazy danych

```bash
python app.py
```

Baza danych zostanie automatycznie utworzona przy pierwszym uruchomieniu.

## 🏃 Uruchomienie

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:5000`

## 📁 Struktura projektu

```
movie_recommender/
├── app/
│   ├── models.py              # Modele bazy danych
│   ├── tmdb_service.py        # Integracja z TMDb API
│   ├── recommendation_engine.py # Algorytmy AI
│   ├── templates/             # Szablony HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── ...
│   └── static/                # Pliki statyczne
│       ├── css/
│       ├── js/
│       └── img/
├── app.py                     # Główna aplikacja Flask
├── config.py                  # Konfiguracja
├── requirements.txt           # Zależności
├── .env.example              # Przykładowy plik środowiskowy
└── README.md                 # Ta dokumentacja
```

## 🤖 Jak działają algorytmy AI

### Content-Based Filtering
1. Analizuje cechy filmów (gatunki, rok)
2. Używa TF-IDF do wektoryzacji cech
3. Oblicza podobieństwo (Cosine Similarity)
4. Rekomenduje filmy podobne do tych, które użytkownik lubił

### Collaborative Filtering
1. Buduje macierz user-movie z ocenami
2. Znajduje podobnych użytkowników (Cosine Similarity)
3. Rekomenduje filmy, które podobni użytkownicy ocenili wysoko

### Hybrid Approach
- 70% waga dla Content-Based
- 30% waga dla Collaborative
- Automatyczne dostosowanie wag w zależności od ilości danych

## 📊 Struktura bazy danych

### Tabela: users
- id, username, email, password_hash, created_at

### Tabela: movies
- id, tmdb_id, title, genres, release_year, overview, poster_path, average_rating

### Tabela: ratings
- id, user_id, movie_id, rating (1.0-5.0), timestamp

### Tabela: watch_history
- id, user_id, movie_id, watched_at

## 🧪 Testowanie

```bash
# Uruchomienie testów jednostkowych
pytest tests/

# Z pokryciem kodu
pytest --cov=app tests/
```

## 📝 Dokumentacja API

### Endpointy

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/` | Strona główna z popularnymi filmami |
| GET/POST | `/register` | Rejestracja użytkownika |
| GET/POST | `/login` | Logowanie |
| GET | `/logout` | Wylogowanie |
| GET | `/dashboard` | Panel użytkownika z rekomendacjami |
| GET | `/search?q=query` | Wyszukiwanie filmów |
| GET | `/movie/<tmdb_id>` | Szczegóły filmu |
| POST | `/rate/<movie_id>` | Oceń film |
| GET | `/my-ratings` | Moje oceny |
| POST | `/add-to-history/<movie_id>` | Dodaj do historii |
| GET | `/my-history` | Historia oglądania |

## 🔐 Bezpieczeństwo

- Hasła są hashowane (Werkzeug SHA256)
- Sesje użytkowników zarządzane przez Flask-Login
- CSRF protection
- Walidacja danych wejściowych

## 🚀 Deployment (opcjonalnie)

### Heroku
```bash
heroku create movie-recommender-app
git push heroku main
```

### PythonAnywhere
1. Załaduj pliki na PythonAnywhere
2. Skonfiguruj WSGI file
3. Ustaw zmienne środowiskowe

## 📈 Dalszy rozwój

Możliwe rozszerzenia:
- [ ] Deep Learning (Neural Collaborative Filtering)
- [ ] Rekomendacje w czasie rzeczywistym
- [ ] Analiza sentymentu recenzji
- [ ] Integracja z dodatkowymi API (IMDb, Rotten Tomatoes)
- [ ] Progressive Web App (PWA)
- [ ] Wielojęzyczność

## 👤 Autor

Praca dyplomowa - Akademia Finansów i Biznesu Vistula, 2026

## 📄 Licencja

Ten projekt został stworzony w celach edukacyjnych.

## 🙏 Podziękowania

- [TMDb API](https://www.themoviedb.org/documentation/api) - za dostęp do danych o filmach
- [Flask](https://flask.palletsprojects.com/) - framework webowy
- [scikit-learn](https://scikit-learn.org/) - biblioteka ML
