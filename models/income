"""
Income Management Module
Track income sources and amounts
"""

from datetime import datetime, date
from config.database import get_connection
import pandas as pd

def add_income(user_id: int, source: str, amount: float, 
               income_date: date, description: str = "") -> dict:
    """
    Add a new income entry
    """
    if amount <= 0:
        return {"success": False, "message": "Amount must be greater than 0"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            INSERT INTO income 
            (user_id, source, amount, income_date, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, source, amount, income_date, description, datetime.now())
        )
        income_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Income added successfully!",
            "income_id": income_id
        }
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error adding income: {str(e)}"}

def get_income(user_id: int, start_date: date = None, end_date: date = None) -> pd.DataFrame:
    """
    Get income entries for a user with optional date filters
    """
    conn = get_connection()
    
    query = """
        SELECT id, source, amount, income_date, description, created_at
        FROM income
        WHERE user_id = ?
    """
    params = [user_id]
    
    if start_date:
        query += " AND income_date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND income_date <= ?"
        params.append(end_date)
    
    query += " ORDER BY income_date DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return df

def get_total_income(user_id: int, month: int = None, year: int = None) -> float:
    """
    Get total income for a period
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT SUM(amount) as total FROM income WHERE user_id = ?"
    params = [user_id]
    
    if month and year:
        query += " AND strftime('%m', income_date) = ? AND strftime('%Y', income_date) = ?"
        params.extend([f"{month:02d}", str(year)])
    elif year:
        query += " AND strftime('%Y', income_date) = ?"
        params.append(str(year))
    
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    
    return float(result['total']) if result['total'] else 0.0

def delete_income(income_id: int, user_id: int) -> dict:
    """
    Delete an income entry
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("SELECT user_id FROM income WHERE id = ?", (income_id,))
    income = cursor.fetchone()
    
    if not income or income['user_id'] != user_id:
        conn.close()
        return {"success": False, "message": "Income entry not found or access denied"}
    
    try:
        cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Income deleted successfully!"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error deleting income: {str(e)}"}

def get_monthly_balance(user_id: int, month: int, year: int) -> dict:
    """
    Calculate monthly balance (income - expenses)
    """
    from models.expense import get_expenses_summary
    
    total_income = get_total_income(user_id, month, year)
    expenses_summary = get_expenses_summary(user_id, month, year)
    total_expenses = expenses_summary['total']
    
    return {
        "income": total_income,
        "expenses": total_expenses,
        "balance": total_income - total_expenses,
        "savings_rate": round((total_income - total_expenses) / total_income * 100, 1) if total_income > 0 else 0
    }

