from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database connection
DATABASE = 'entertainment.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            flash('All fields are required!')
            return redirect(url_for('register'))

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email.')
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
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials! Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Sample articles for display
    articles = [
        {"title": "New Music Album Released", "content": "Details about the new album released.", "image_url": "/static/images/news1.jpg", "link": "/article/1"},
        {"title": "Hollywood Stars News", "content": "Latest news about Hollywood stars.", "image_url": "/static/images/news2.jpg", "link": "/article/2"},
        # Add more articles here
    ]
    
    return render_template('home.html', articles=articles)

@app.route('/music')
def music():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    trending_songs = [
        {"title": "Song 1", "description": "Amazing new song.", "image_url": "/static/images/song1.jpg", "spotify_link": "#", "youtube_link": "#", "apple_music_link": "#"},
        {"title": "Song 2", "description": "Another great song.", "image_url": "/static/images/song2.jpg", "spotify_link": "#", "youtube_link": "#", "apple_music_link": "#"},
        # Add more songs here
    ]

    upcoming_releases = [
        {"title": "Upcoming Release 1", "description": "Release details", "image_url": "/static/images/upcoming1.jpg"},
        {"title": "Upcoming Release 2", "description": "Release details", "image_url": "/static/images/upcoming2.jpg"},
        # Add upcoming releases here
    ]

    return render_template('music.html', trending_songs=trending_songs, upcoming_releases=upcoming_releases)

@app.route('/movies')
def movies():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    movies = [
        {"title": "Movie 1", "description": "Description of Movie 1", "thumbnail_url": "/static/images/movie1.jpg", "trailer_link": "https://www.youtube.com/watch?v=trailer1"},
        {"title": "Movie 2", "description": "Description of Movie 2", "thumbnail_url": "/static/images/movie2.jpg", "trailer_link": "https://www.youtube.com/watch?v=trailer2"},
        # Add more movies here
    ]
    
    return render_template('movies.html', movies=movies)

@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    events = [
        {"name": "Live Concert", "date": "2024-12-15", "image_url": "/static/images/concert.jpg"},
        {"name": "Film Festival", "date": "2024-01-10", "image_url": "/static/images/film_festival.jpg"},
        # Add more events here
    ]

    return render_template('events.html', events=events)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/book_event/<event_id>', methods=['POST'])
def book_event(event_id):
    if 'user_id' not in session:
        return {'success': False, 'message': 'You need to be logged in to book an event.'}, 403

    conn = get_db_connection()
    
    # Check if event exists
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()

    if event:
        # Store the booking information
        conn.execute('INSERT INTO bookings (user_id, event_id) VALUES (?, ?)', (session['user_id'], event_id))
        conn.commit()
        conn.close()
        
        return {'success': True, 'eventName': event['name']}
    else:
        conn.close()
        return {'success': False, 'message': 'Event not found.'}
@app.route('/book_event/<event_id>', methods=['POST'])
def book_event(event_id):
    if 'user_id' not in session:
        return {'success': False, 'message': 'You need to be logged in to book an event.'}, 403

    conn = get_db_connection()
    
    # Check if event exists
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()

    if event:
        # Store the booking information
        conn.execute('INSERT INTO bookings (user_id, event_id) VALUES (?, ?)', (session['user_id'], event_id))
        conn.commit()
        conn.close()
        
        return {'success': True, 'eventName': event['name']}
    else:
        conn.close()
        return {'success': False, 'message': 'Event not found.'}