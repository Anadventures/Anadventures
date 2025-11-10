"""
Database initialization script
Run this once to create the database schema
"""
from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully!")
    print("📁 Database location: instance/user-data.sqlite3")

