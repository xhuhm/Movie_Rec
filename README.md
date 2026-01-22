# Movie_Rec

# 🎬 Movie Recommendation System

Aplikacja webowa z systemem rekomendacji filmów opartym na algorytmach sztucznej inteligencji.

**Praca dyplomowa** - Akademia Finansów i Biznesu Vistula, 2026  
**Autor:** Mykyta Tolok (nr albumu: 63657)  
**Promotor:** dr Weronika Figura

---

## 📖 Opis

System analizuje preferencje użytkowników i generuje spersonalizowane rekomendacje filmowe. Wykorzystuje hybrydowy algorytm łączący filtrowanie oparte na treści (Content-Based) oraz filtrowanie kolaboratywne (Collaborative Filtering).

**Trafność rekomendacji:** ~70%

---

## 🛠️ Technologie

### Backend
- Python 3.10
- Flask (framework webowy)
- SQLite (baza danych)
- SQLAlchemy (ORM)

### Machine Learning
- pandas (analiza danych)
- numpy (operacje numeryczne)
- scikit-learn (TF-IDF, cosine similarity)

### Frontend
- HTML5 / CSS3 / JavaScript
- Bootstrap 5 (responsywny UI)
- Jinja2 (szablony)

### API
- The Movie Database (TMDb) - źródło danych filmowych

---

## ⚙️ Instalacja i uruchomienie

### 1. Sklonuj repozytorium
```bash
git clone https://github.com/twoj-username/movie-recommender.git
cd movie-recommender
```

### 2. Utwórz środowisko wirtualne
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 4. Skonfiguruj plik .env
Utwórz plik `.env` w głównym katalogu:
```
TMDB_API_KEY=twoj_klucz_api_z_tmdb
SECRET_KEY=losowy_ciag_znakow
```

Klucz API można uzyskać bezpłatnie na: https://www.themoviedb.org/settings/api

### 5. Uruchom aplikację
```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: **http://localhost:5000**

---

## 🎯 Jak korzystać

1. **Zarejestruj się** - utwórz nowe konto
2. **Zaloguj się** - wpisz email i hasło
3. **Przeglądaj filmy** - zobacz popularne tytuły z TMDb
4. **Oceń filmy** - wystaw oceny 1-5 gwiazdek (minimum 3-5 filmów)
5. **Zobacz rekomendacje** - kliknij "Dla Ciebie" w menu

System automatycznie wygeneruje spersonalizowane sugestie filmowe na podstawie Twoich ocen.

---

## 🤖 Algorytm AI

System wykorzystuje **hybrydowe podejście**:

- **Content-Based Filtering** (70% wagi) - analizuje gatunki i cechy filmów
- **Collaborative Filtering** (30% wagi) - znajduje podobnych użytkowników

**Wzór podobieństwa:**
```
similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Dla nowych użytkowników system automatycznie używa tylko Content-Based (cold start handling).

---

## 📁 Struktura projektu

```
├── app.py                      # Główny plik aplikacji + routing
├── models.py                   # Modele bazy danych
├── recommendation_engine.py    # Algorytmy AI
├── tmdb_service.py            # Integracja z TMDb API
├── requirements.txt            # Zależności
├── templates/                  # Szablony HTML
└── static/                     # CSS, JS
```

---

## 📄 Licencja

MIT License - projekt edukacyjny (praca dyplomowa)

**Copyright © 2026 Mykyta Tolok**
