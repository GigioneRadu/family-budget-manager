"""
Authentication utilities
Password hashing, session management, user operations
"""

import hashlib
import secrets
from datetime import datetime
from config.database import get_connection

def hash_password(password: str, salt: str = None) -> tuple:
    """
    Hash password using SHA-256 with salt
    Returns: (hash, salt)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    # Combine password and salt, then hash
    pwd_salt = f"{password}{salt}"
    password_hash = hashlib.sha256(pwd_salt.encode()).hexdigest()
    
    return password_hash, salt

def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify password against stored hash
    Format of stored_hash: "salt:hash"
    """
    try:
        salt, hash_value = stored_hash.split(':')
        computed_hash, _ = hash_password(password, salt)
        return computed_hash == hash_value
    except:
        return False

def register_user(username: str, password: str, email: str = None) -> dict:
    """
    Register a new user
    Returns: {"success": bool, "message": str, "user_id": int}
    """
    # Validate input
    if not username or len(username) < 3:
        return {"success": False, "message": "Username must be at least 3 characters long"}
    
    if not password or len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters long"}
    
    # Hash password
    pwd_hash, salt = hash_password(password)
    stored_hash = f"{salt}:{pwd_hash}"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert user
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, created_at) VALUES (?, ?, ?, ?)",
            (username, stored_hash, email, datetime.now())
        )
        user_id = cursor.lastrowid
        
        # Create default user preferences
        cursor.execute(
            "INSERT INTO user_preferences (user_id) VALUES (?)",
            (user_id,)
        )
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Account created successfully!",
            "user_id": user_id
        }
    
    except Exception as e:
        conn.close()
        if "UNIQUE constraint failed" in str(e):
            return {"success": False, "message": "Username already exists"}
        return {"success": False, "message": f"Error creating account: {str(e)}"}

def login_user(username: str, password: str) -> dict:
    """
    Authenticate user
    Returns: {"success": bool, "message": str, "user_id": int, "username": str}
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return {"success": False, "message": "Invalid username or password"}
        
        # Verify password
        if verify_password(password, user['password_hash']):
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now(), user['id'])
            )
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": "Login successful!",
                "user_id": user['id'],
                "username": user['username']
            }
        else:
            conn.close()
            return {"success": False, "message": "Invalid username or password"}
    
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Login error: {str(e)}"}

def get_user_info(user_id: int) -> dict:
    """
    Get user information
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT u.id, u.username, u.email, u.created_at, u.last_login,
               p.currency, p.language, p.theme, p.notifications
        FROM users u
        LEFT JOIN user_preferences p ON u.id = p.user_id
        WHERE u.id = ?
        """,
        (user_id,)
    )
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def update_user_preferences(user_id: int, **kwargs) -> bool:
    """
    Update user preferences
    kwargs can include: currency, language, theme, notifications
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build update query dynamically
    fields = []
    values = []
    
    for key, value in kwargs.items():
        if key in ['currency', 'language', 'theme', 'notifications']:
            fields.append(f"{key} = ?")
            values.append(value)
    
    if not fields:
        return False
    
    values.append(user_id)
    query = f"UPDATE user_preferences SET {', '.join(fields)} WHERE user_id = ?"
    
    try:
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

