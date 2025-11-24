import sqlite3
from flask import g

DATABASE = 'connect.db'


def get_db():
    """Get a database connection (stored on flask.g for request lifetime)"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # allows dict-like access: row['name']
    return db


def close_db(error=None):
    """Close the database connection at the end of request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db(app):
    """Create the messages table if it doesn't exist"""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                message TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        print("Database initialized – table 'messages' ready")


def save_message(name: str, email: str, contact_number: str, message: str) -> int:
    """Insert a new message and return the new row ID"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO messages (name, email, contact_number, message) VALUES (?, ?, ?, ?)",
        (name, email, contact_number, message)
    )
    db.commit()


def get_messages_paginated(page: int = 1, per_page: int = 10):
    """
    Returns:
        - rows: list of messages for the current page
        - total: total number of messages
        - total_pages: how many pages exist
    """
    db = get_db()
    
    # Get total count
    total = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    
    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page
    
    # Calculate page offset
    if page > total_pages and total_pages > 0:
        page = total_pages
    offset = (page - 1) * per_page
    
    # Fetch current page
    rows = db.execute(
        "SELECT * FROM messages ORDER BY submitted_at DESC LIMIT ? OFFSET ?",
        (per_page, offset)
    ).fetchall()
    
    return {
        "rows": rows,
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "per_page": per_page,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None
    }