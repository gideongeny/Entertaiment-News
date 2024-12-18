-- User table for registration and login
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- News table for dynamic content
CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image_url TEXT,
    category TEXT NOT NULL
);

-- Events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    image_url TEXT
);
-- Bookings table
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

INSERT INTO events (name, description, date, image_url) VALUES 
('Live Concert by The Weeknd', 'Experience an electrifying live performance!', '2024-12-15', 'static/images/concert.jpg'),
('2024 Film Festival', 'Join us for an unforgettable film celebration.', '2024-01-10', 'static/images/film-festival.jpg');
