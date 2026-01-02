"""
Expense Management Module
CRUD operations for expenses
"""

from datetime import datetime, date
from config.database import get_connection
import pandas as pd

def add_expense(user_id: int, category: str, subcategory: str, amount: float, 
                expense_date: date, description: str = "", tags: str = "") -> dict:
    """
    Add a new expense
    Returns: {"success": bool, "message": str, "expense_id": int}
    """
    if amount <= 0:
        return {"success": False, "message": "Amount must be greater than 0"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            INSERT INTO expenses 
            (user_id, category, subcategory, amount, expense_date, description, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, category, subcategory, amount, expense_date, description, tags, datetime.now())
        )
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": "Expense added successfully!",
            "expense_id": expense_id
        }
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error adding expense: {str(e)}"}

def get_expenses(user_id: int, start_date: date = None, end_date: date = None, 
                 category: str = None, limit: int = None) -> pd.DataFrame:
    """
    Get expenses for a user with optional filters
    Returns: DataFrame with expenses
    """
    conn = get_connection()
    
    query = """
        SELECT id, category, subcategory, amount, expense_date, 
               description, tags, created_at
        FROM expenses
        WHERE user_id = ?
    """
    params = [user_id]
    
    if start_date:
        query += " AND expense_date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND expense_date <= ?"
        params.append(end_date)
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    query += " ORDER BY expense_date DESC"
    
    if limit:
        query += f" LIMIT {limit}"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return df

def update_expense(expense_id: int, user_id: int, **kwargs) -> dict:
    """
    Update an expense
    kwargs can include: category, subcategory, amount, expense_date, description, tags
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("SELECT user_id FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    
    if not expense or expense['user_id'] != user_id:
        conn.close()
        return {"success": False, "message": "Expense not found or access denied"}
    
    # Build update query
    fields = []
    values = []
    
    allowed_fields = ['category', 'subcategory', 'amount', 'expense_date', 'description', 'tags']
    for key, value in kwargs.items():
        if key in allowed_fields:
            fields.append(f"{key} = ?")
            values.append(value)
    
    if not fields:
        conn.close()
        return {"success": False, "message": "No fields to update"}
    
    fields.append("updated_at = ?")
    values.append(datetime.now())
    values.append(expense_id)
    
    query = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
    
    try:
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return {"success": True, "message": "Expense updated successfully!"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error updating expense: {str(e)}"}

def delete_expense(expense_id: int, user_id: int) -> dict:
    """
    Delete an expense
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("SELECT user_id FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    
    if not expense or expense['user_id'] != user_id:
        conn.close()
        return {"success": False, "message": "Expense not found or access denied"}
    
    try:
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Expense deleted successfully!"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error deleting expense: {str(e)}"}

def get_expenses_summary(user_id: int, month: int = None, year: int = None) -> dict:
    """
    Get expenses summary by category
    """
    conn = get_connection()
    
    query = """
        SELECT category, 
               SUM(amount) as total_amount,
               COUNT(*) as count
        FROM expenses
        WHERE user_id = ?
    """
    params = [user_id]
    
    if month and year:
        query += " AND strftime('%m', expense_date) = ? AND strftime('%Y', expense_date) = ?"
        params.extend([f"{month:02d}", str(year)])
    elif year:
        query += " AND strftime('%Y', expense_date) = ?"
        params.append(str(year))
    
    query += " GROUP BY category ORDER BY total_amount DESC"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    if df.empty:
        return {"total": 0, "by_category": {}}
    
    return {
        "total": float(df['total_amount'].sum()),
        "by_category": df.set_index('category')['total_amount'].to_dict()
    }

def get_monthly_trend(user_id: int, months: int = 6) -> pd.DataFrame:
    """
    Get monthly spending trend for the last N months
    """
    conn = get_connection()
    
    query = """
        SELECT 
            strftime('%Y-%m', expense_date) as month,
            category,
            SUM(amount) as total_amount
        FROM expenses
        WHERE user_id = ?
        AND expense_date >= date('now', ?)
        GROUP BY month, category
        ORDER BY month DESC, category
    """
    
    df = pd.read_sql_query(query, conn, params=[user_id, f'-{months} months'])
    conn.close()
    
    return df

