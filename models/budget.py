"""
Budget Planning Module
Manage monthly budget plans and compare with actual spending
"""

from datetime import datetime
from config.database import get_connection
import pandas as pd

def set_budget(user_id: int, category: str, subcategory: str, 
               planned_amount: float, month: int, year: int) -> dict:
    """
    Set or update budget plan for a category/subcategory
    """
    if planned_amount < 0:
        return {"success": False, "message": "Budget amount cannot be negative"}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if budget already exists
        cursor.execute(
            """
            SELECT id FROM budget_plans 
            WHERE user_id = ? AND category = ? AND subcategory = ? 
            AND month = ? AND year = ?
            """,
            (user_id, category, subcategory, month, year)
        )
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing budget
            cursor.execute(
                """
                UPDATE budget_plans 
                SET planned_amount = ?
                WHERE id = ?
                """,
                (planned_amount, existing['id'])
            )
            message = "Budget updated successfully!"
        else:
            # Insert new budget
            cursor.execute(
                """
                INSERT INTO budget_plans 
                (user_id, category, subcategory, planned_amount, month, year, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, category, subcategory, planned_amount, month, year, datetime.now())
            )
            message = "Budget set successfully!"
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": message}
    
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error setting budget: {str(e)}"}

def get_budget(user_id: int, month: int, year: int) -> pd.DataFrame:
    """
    Get budget plan for a specific month
    """
    conn = get_connection()
    
    query = """
        SELECT category, subcategory, planned_amount
        FROM budget_plans
        WHERE user_id = ? AND month = ? AND year = ?
        ORDER BY category, subcategory
    """
    
    df = pd.read_sql_query(query, conn, params=[user_id, month, year])
    conn.close()
    
    return df

def get_budget_vs_actual(user_id: int, month: int, year: int) -> pd.DataFrame:
    """
    Compare budgeted amounts vs actual spending
    Returns DataFrame with: category, subcategory, planned, actual, difference, percentage
    """
    conn = get_connection()
    
    query = """
        SELECT 
            bp.category,
            bp.subcategory,
            bp.planned_amount,
            COALESCE(SUM(e.amount), 0) as actual_amount
        FROM budget_plans bp
        LEFT JOIN expenses e ON 
            bp.user_id = e.user_id AND
            bp.category = e.category AND
            bp.subcategory = e.subcategory AND
            strftime('%m', e.expense_date) = ? AND
            strftime('%Y', e.expense_date) = ?
        WHERE bp.user_id = ? AND bp.month = ? AND bp.year = ?
        GROUP BY bp.category, bp.subcategory, bp.planned_amount
        ORDER BY bp.category, bp.subcategory
    """
    
    df = pd.read_sql_query(
        query, 
        conn, 
        params=[f"{month:02d}", str(year), user_id, month, year]
    )
    conn.close()
    
    if not df.empty:
        df['difference'] = df['planned_amount'] - df['actual_amount']
        df['percentage'] = (df['actual_amount'] / df['planned_amount'] * 100).round(1)
        df['status'] = df.apply(
            lambda row: 'Over Budget' if row['actual_amount'] > row['planned_amount'] else 'On Track',
            axis=1
        )
    
    return df

def get_category_budget_summary(user_id: int, month: int, year: int) -> dict:
    """
    Get budget summary by main category
    """
    conn = get_connection()
    
    query = """
        SELECT 
            bp.category,
            SUM(bp.planned_amount) as total_planned,
            COALESCE(SUM(e.amount), 0) as total_actual
        FROM budget_plans bp
        LEFT JOIN expenses e ON 
            bp.user_id = e.user_id AND
            bp.category = e.category AND
            strftime('%m', e.expense_date) = ? AND
            strftime('%Y', e.expense_date) = ?
        WHERE bp.user_id = ? AND bp.month = ? AND bp.year = ?
        GROUP BY bp.category
        ORDER BY total_planned DESC
    """
    
    df = pd.read_sql_query(
        query,
        conn,
        params=[f"{month:02d}", str(year), user_id, month, year]
    )
    conn.close()
    
    if df.empty:
        return {
            "total_planned": 0,
            "total_actual": 0,
            "total_difference": 0,
            "categories": []
        }
    
    total_planned = float(df['total_planned'].sum())
    total_actual = float(df['total_actual'].sum())
    
    categories = []
    for _, row in df.iterrows():
        categories.append({
            "category": row['category'],
            "planned": float(row['total_planned']),
            "actual": float(row['total_actual']),
            "difference": float(row['total_planned'] - row['total_actual']),
            "percentage": round(row['total_actual'] / row['total_planned'] * 100, 1) if row['total_planned'] > 0 else 0
        })
    
    return {
        "total_planned": total_planned,
        "total_actual": total_actual,
        "total_difference": total_planned - total_actual,
        "categories": categories
    }

def delete_budget(user_id: int, category: str, subcategory: str, month: int, year: int) -> dict:
    """
    Delete a budget entry
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            DELETE FROM budget_plans 
            WHERE user_id = ? AND category = ? AND subcategory = ? 
            AND month = ? AND year = ?
            """,
            (user_id, category, subcategory, month, year)
        )
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Budget deleted successfully!"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error deleting budget: {str(e)}"}

def copy_budget_to_next_month(user_id: int, from_month: int, from_year: int) -> dict:
    """
    Copy current month's budget to next month
    """
    # Calculate next month
    next_month = from_month + 1
    next_year = from_year
    if next_month > 12:
        next_month = 1
        next_year += 1
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get current month's budget
        cursor.execute(
            """
            SELECT category, subcategory, planned_amount
            FROM budget_plans
            WHERE user_id = ? AND month = ? AND year = ?
            """,
            (user_id, from_month, from_year)
        )
        
        budgets = cursor.fetchall()
        
        if not budgets:
            conn.close()
            return {"success": False, "message": "No budget found for the selected month"}
        
        # Insert into next month (ignore duplicates)
        for budget in budgets:
            cursor.execute(
                """
                INSERT OR IGNORE INTO budget_plans 
                (user_id, category, subcategory, planned_amount, month, year, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, budget['category'], budget['subcategory'], 
                 budget['planned_amount'], next_month, next_year, datetime.now())
            )
        
        conn.commit()
        conn.close()
        
        return {
            "success": True, 
            "message": f"Budget copied to {next_month}/{next_year}",
            "next_month": next_month,
            "next_year": next_year
        }
    
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error copying budget: {str(e)}"}

