from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.secret_key = 'your-secure-random-secret-key-here'

# OMDb API Configuration (You already have this!)
OMDB_API_KEY = '90998eb3'  # Your existing API key
OMDB_BASE_URL = 'http://www.omdbapi.com/'

# Load datasets
def load_datasets():
    hollywood_df = pd.read_csv('dataset.csv')
    try:
        bollywood_df = pd.read_csv('bollywood.csv')
    except FileNotFoundError:
        bollywood_df = pd.DataFrame()
    try:
        webseries_df = pd.read_csv('webseries.csv')
    except FileNotFoundError:
        webseries_df = pd.DataFrame()
    return hollywood_df, bollywood_df, webseries_df

hollywood_movies, bollywood_movies, webseries = load_datasets()

# Precompute ALL_MOVIES to save time
dfs = []
if not hollywood_movies.empty:
    hollywood_copy = hollywood_movies.copy()
    hollywood_copy['category'] = 'Hollywood'
    dfs.append(hollywood_copy)
if not bollywood_movies.empty:
    bollywood_copy = bollywood_movies.copy()
    bollywood_copy['category'] = 'Bollywood'
    dfs.append(bollywood_copy)
if not webseries.empty:
    webseries_copy = webseries.copy()
    webseries_copy['category'] = 'Web Series'
    dfs.append(webseries_copy)

ALL_MOVIES_DF = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def get_all_movies():
    return ALL_MOVIES_DF

# Cache OMDB API calls
@lru_cache(maxsize=2000)
def get_omdb_details(movie_title):
    try:
        url = OMDB_BASE_URL
        params = {
            'apikey': OMDB_API_KEY,
            't': movie_title,
            'plot': 'full'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('Response') == 'True':
            poster = data.get('Poster') if data.get('Poster') != 'N/A' else None
            cast = data.get('Actors', '').split(', ')[:5] if data.get('Actors') != 'N/A' else []
            director = data.get('Director', 'N/A')
            imdb_id = data.get('imdbID')
            imdb_link = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else None
            
            runtime_str = data.get('Runtime', 'N/A')
            runtime = int(runtime_str.split()[0]) if runtime_str != 'N/A' and runtime_str.split()[0].isdigit() else None
            
            release_date = data.get('Released', 'N/A')
            
            return {
                'poster': poster,
                'cast': cast,
                'director': director,
                'imdb_link': imdb_link,
                'runtime': runtime,
                'release_date': release_date,
                'plot': data.get('Plot', ''),
                'rated': data.get('Rated', 'N/A'),
                'awards': data.get('Awards', 'N/A'),
                'trailer': None
            }
    except Exception as e:
        print(f"OMDb API Error: {e}")
    return None

# Parallel fetching for faster loading
def add_posters_to_movies(movies_list):
    def fetch_poster(movie):
        omdb_data = get_omdb_details(movie['title'])
        movie['poster'] = omdb_data['poster'] if omdb_data else None
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(fetch_poster, movies_list)

# Precompute TF-IDF matrices to save time during recommendation
tfidf_matrices = {}
def get_tfidf_matrix(category, dataset):
    if category not in tfidf_matrices:
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrices[category] = tfidf.fit_transform(dataset['overview'].fillna(''))
    return tfidf_matrices[category]

@lru_cache(maxsize=100)
def get_recommendation_indices(movie_title, category):
    if category == 'Hollywood':
        dataset = hollywood_movies
    elif category == 'Bollywood':
        dataset = bollywood_movies
    else:
        dataset = webseries
        
    if dataset.empty or movie_title not in dataset['title'].values:
        return []
        
    tfidf_matrix = get_tfidf_matrix(category, dataset)
    movie_idx = dataset[dataset['title'] == movie_title].index[0]
    similarity_scores = cosine_similarity(tfidf_matrix[movie_idx], tfidf_matrix).flatten()
    
    # Return indices instead of full rows so we can cache it easily
    # We get top 20 just in case we need more, but limit it later
    similar_idx = similarity_scores.argsort()[-(20 + 1):-1][::-1]
    return similar_idx.tolist()

def recommend_movies(movie_title, dataset, category, num_recommendations=8):
    if dataset.empty:
        return []
    
    similar_idx = get_recommendation_indices(movie_title, category)
    if not similar_idx:
        return []
        
    # Trim to requested number
    similar_idx = similar_idx[:num_recommendations]
    recommendations = dataset.iloc[similar_idx][['title', 'genre']].to_dict('records')
    
    add_posters_to_movies(recommendations)
    return recommendations

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    all_movies = get_all_movies()
    if not all_movies.empty and 'popularity' in all_movies.columns:
        popular = all_movies.nlargest(12, 'popularity')[['title', 'genre', 'vote_average', 'category']].to_dict('records')
        add_posters_to_movies(popular)
    else:
        popular = []
    
    return render_template('index.html', movies=popular, username=session.get('username'))

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('welcome.html')

@app.route('/hollywood')
def hollywood():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    movies = hollywood_movies.head(20)[['title', 'genre', 'vote_average']].to_dict('records')
    add_posters_to_movies(movies)
    
    return render_template('category.html', movies=movies, category='Hollywood', username=session.get('username'))

@app.route('/bollywood')
def bollywood():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    if bollywood_movies.empty:
        return render_template('category.html', movies=[], category='Bollywood', 
                             message="Bollywood dataset coming soon!", username=session.get('username'))
    
    movies = bollywood_movies.head(20)[['title', 'genre', 'votes']].to_dict('records')
    add_posters_to_movies(movies)
    
    return render_template('category.html', movies=movies, category='Bollywood', username=session.get('username'))

@app.route('/webseries')
def web_series():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    if webseries.empty:
        return render_template('category.html', movies=[], category='Web Series', 
                             message="Web Series dataset coming soon!", username=session.get('username'))
    
    series = webseries.head(20)[['title', 'genre', 'vote_count']].to_dict('records')
    add_posters_to_movies(series)
    
    return render_template('category.html', movies=series, category='Web Series', username=session.get('username'))

@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    query = request.args.get('q', '').lower()
    all_movies = get_all_movies()
    
    if query and not all_movies.empty:
        results = all_movies[all_movies['title'].str.lower().str.contains(query, na=False)]
        movies = results[['title', 'genre', 'vote_average', 'category']].head(20).to_dict('records')
        add_posters_to_movies(movies)
    else:
        movies = []
    
    return render_template('search.html', movies=movies, query=query, username=session.get('username'))


@app.route('/filter')
def filter_movies():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    all_movies = get_all_movies()
    
    genre = request.args.get('genre', '')
    min_rating_str = request.args.get('min_rating')
    category = request.args.get('category', '')
    
    filtered = all_movies.copy()
    
    if genre and 'genre' in filtered.columns:
        filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]
    
    if min_rating_str and 'vote_average' in filtered.columns:
        try:
            min_rating = float(min_rating_str)
            numeric_vote_average = pd.to_numeric(filtered['vote_average'], errors='coerce')
            filtered = filtered[numeric_vote_average >= min_rating]
        except(ValueError, TypeError):
            pass
    
    if category and category.strip() and 'category' in filtered.columns:
        filtered = filtered[filtered['category'] == category]
    
    movies = filtered[['title', 'genre', 'vote_average', 'category']].head(20).to_dict('records')
    add_posters_to_movies(movies)
    
    if 'genre' in all_movies.columns:
        # Avoid SettingWithCopyWarning by copying just the column or using the full dataframe properly
        all_movies_copy = all_movies.copy()
        all_movies_copy['genre'] = all_movies_copy['genre'].astype(str)
        genres = sorted(all_movies_copy['genre'].str.split(',').explode().str.strip().unique().tolist())
    else:
        genres = []
    
    return render_template('filter.html', movies=movies, genres=genres, username=session.get('username'))

@app.route('/movie/<path:movie_title>')
def movie_detail(movie_title):
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    all_movies = get_all_movies()
    movie_data = all_movies[all_movies['title'] == movie_title]
    
    if movie_data.empty:
        return "Movie not found", 404
    
    movie = movie_data.iloc[0].to_dict()
    
    omdb_data = get_omdb_details(movie_title)
    if omdb_data:
        movie.update(omdb_data)
    
    category = movie.get('category', 'Hollywood')
    dataset = pd.DataFrame()
    if category == 'Hollywood':
        dataset = hollywood_movies
    elif category == 'Bollywood':
        dataset = bollywood_movies
    else:
        dataset = webseries
    
    recommendations = recommend_movies(movie_title, dataset, category, num_recommendations=8)
    
    return render_template('movie_detail.html', movie=movie, recommendations=recommendations, username=session.get('username'))

@app.route('/recommend')
def recommend():
    if 'username' not in session:
        return redirect(url_for('welcome'))

    query = request.args.get('q', '')
    recommendations = []
    
    if query:
        all_movies = get_all_movies()
        movie_data = all_movies[all_movies['title'].str.lower() == query.lower()]

        if not movie_data.empty:
            movie_title = movie_data.iloc[0]['title']
            category = movie_data.iloc[0].get('category', 'Hollywood')
            
            if category == 'Hollywood':
                dataset = hollywood_movies
            elif category == 'Bollywood':
                dataset = bollywood_movies
            else:
                dataset = webseries
            
            recommendations = recommend_movies(movie_title, dataset, category, num_recommendations=12)

    return render_template('recommendations.html', recommendations=recommendations, query=query, username=session.get('username'))

@app.context_processor
def inject_current_path():
    return {'current_path': request.path}

@app.route('/about')
def about():
    return render_template('about.html', username=session.get('username', ''))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
