from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import requests
from functools import wraps

import os

app = Flask(__name__)
app.secret_key = 'paparazzi_secret_key'

# Database connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'entertainment.db')

# API Configurations (In a real app, these should be in environment variables)
# NewsAPI key should be replaced with a real one
NEWS_API_KEY = 'YOUR_NEWSAPI_KEY' 
TMDB_API_KEY = 'YOUR_TMDB_API_KEY'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('register'))
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    # Fetch live news from NewsAPI
    # Note: If no API key is provided, we'll fall back to sample data
    articles = []
    try:
        url = f'https://newsapi.org/v2/top-headlines?category=entertainment&language=en&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            for item in news_data.get('articles', []):
                articles.append({
                    "title": item.get('title'),
                    "content": item.get('description') or "No description available.",
                    "image_url": item.get('urlToImage') or "/static/images/news-placeholder.jpg",
                    "link": item.get('url')
                })
        
        if not articles:
            raise Exception("No articles found")
            
    except Exception as e:
        # Fallback to high-quality sample data if API fails or no key
        articles = [
            {
                "title": "Oscars 2026: The Frontrunners for Best Picture",
                "content": "A deep dive into the films leading the race for Hollywood's biggest night.",
                "image_url": "https://images.unsplash.com/photo-1594908900066-3f47337549d8?auto=format&fit=crop&q=80&w=1000",
                "link": "#"
            },
            {
                "title": "Global Tour: Legends Return to the Stage",
                "content": "From London to Tokyo, the world's biggest icons are hitting the road this summer.",
                "image_url": "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?auto=format&fit=crop&q=80&w=1000",
                "link": "#"
            },
            {
                "title": "The Evolution of Streaming: What's Next for Cinema?",
                "content": "How digital platforms are reshaping the way we experience movies.",
                "image_url": "https://images.unsplash.com/photo-1524712245354-2c4e5e7121c0?auto=format&fit=crop&q=80&w=1000",
                "link": "#"
            }
        ]
    
    return render_template('home.html', articles=articles)

@app.route('/music')
@login_required
def music():
    # Using Last.fm or similar would be ideal, but for now, we'll use premium curated data
    trending_songs = [
        {"title": "Midnight City", "artist": "The Dreamers", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=500"},
        {"title": "Neon Lights", "artist": "Synth Wave", "image_url": "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&q=80&w=500"},
        {"title": "Echoes of Silence", "artist": "Luna Bloom", "image_url": "https://images.unsplash.com/photo-1459749411177-042180ce673c?auto=format&fit=crop&q=80&w=500"}
    ]
    return render_template('music.html', trending_songs=trending_songs)

@app.route('/movies')
@login_required
def movies():
    # Fetch from TMDB if key exists
    movies = []
    try:
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1'
        response = requests.get(url)
        if response.status_code == 200:
            movie_data = response.json()
            for movie in movie_data.get('results', []):
                movies.append({
                    "title": movie.get('title'),
                    "description": movie.get('overview'),
                    "thumbnail_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
                    "link": f"https://www.themoviedb.org/movie/{movie.get('id')}"
                })
        if not movies:
            raise Exception("No movies found")
    except:
        movies = [
            {"title": "The Silent Star", "description": "An interstellar journey beyond the known universe.", "thumbnail_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=500", "link": "#"},
            {"title": "Emerald City", "description": "A futuristic thriller set in a world where nature has taken over.", "thumbnail_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&q=80&w=500", "link": "#"}
        ]
    
    return render_template('movies.html', movies=movies)

@app.route('/events')
@login_required
def events():
    events = [
        {"name": "Gala of Lights", "date": "Dec 15, 2026", "image_url": "https://images.unsplash.com/photo-1540575861501-7c0011e39f5f?auto=format&fit=crop&q=80&w=800"},
        {"name": "Cannes Film Festival", "date": "May 12, 2026", "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&q=80&w=800"}
    ]
    return render_template('events.html', events=events)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)