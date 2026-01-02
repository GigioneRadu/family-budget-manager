"""
Database Configuration and Setup
Supports both SQLite (local dev) and PostgreSQL (production)
"""

import sqlite3
import os
from datetime import datetime

# Database path for SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'family_budget.db')

# For PostgreSQL (Supabase) - set these in Streamlit secrets
# DATABASE_URL = os.getenv('DATABASE_URL', None)

def get_connection():
    """
    Returns database connection
    Uses PostgreSQL if DATABASE_URL is set, otherwise SQLite
    """
    # For now, we'll use SQLite. Later we can add PostgreSQL support
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_database():
    """
    Initialize database tables
    Creates all necessary tables if they don't exist
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table with hashed passwords
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Budget plans table (monthly budget planning)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            planned_amount REAL NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, category, subcategory, month, year)
        )
    ''')
    
    # Expenses table (actual expenses)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            expense_date DATE NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Income table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            income_date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # User preferences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            currency TEXT DEFAULT 'USD',
            language TEXT DEFAULT 'en',
            theme TEXT DEFAULT 'light',
            notifications BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id)
        )
    ''')
    
    # AI predictions cache (for ML predictions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            predicted_amount REAL NOT NULL,
            confidence REAL,
            prediction_month INTEGER NOT NULL,
            prediction_year INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")

def reset_database():
    """
    WARNING: Deletes all data and recreates tables
    Use only for development/testing
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Old database deleted")
    init_database()

if __name__ == "__main__":
    # Initialize database when running this file directly
    init_database()

