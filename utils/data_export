"""
Data Export Utilities
Export data to CSV, Excel, and prepare for backup/restore
"""

import pandas as pd
from datetime import datetime
import io
import json
from models.expense import get_expenses
from models.income import get_income
from models.budget import get_budget

def export_expenses_to_csv(user_id: int, start_date=None, end_date=None) -> bytes:
    """
    Export expenses to CSV format
    Returns: CSV data as bytes
    """
    df = get_expenses(user_id, start_date, end_date)
    
    if df.empty:
        return None
    
    # Convert to CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue().encode('utf-8')

def export_expenses_to_excel(user_id: int, start_date=None, end_date=None) -> bytes:
    """
    Export expenses to Excel format with multiple sheets
    Returns: Excel file as bytes
    """
    excel_buffer = io.BytesIO()
    
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        # Expenses sheet
        df_expenses = get_expenses(user_id, start_date, end_date)
        if not df_expenses.empty:
            df_expenses.to_excel(writer, sheet_name='Expenses', index=False)
        
        # Income sheet
        df_income = get_income(user_id, start_date, end_date)
        if not df_income.empty:
            df_income.to_excel(writer, sheet_name='Income', index=False)
        
        # Summary by category
        if not df_expenses.empty:
            summary = df_expenses.groupby('category')['amount'].agg(['sum', 'count', 'mean'])
            summary.columns = ['Total Amount', 'Count', 'Average']
            summary = summary.round(2)
            summary.to_excel(writer, sheet_name='Summary')
    
    excel_buffer.seek(0)
    return excel_buffer.getvalue()

def create_full_backup(user_id: int) -> dict:
    """
    Create a complete backup of user data
    Returns: Dictionary with all user data
    """
    from models.expense import get_expenses
    from models.income import get_income
    from config.database import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all expenses
    df_expenses = get_expenses(user_id)
    expenses = df_expenses.to_dict('records') if not df_expenses.empty else []
    
    # Get all income
    df_income = get_income(user_id)
    income = df_income.to_dict('records') if not df_income.empty else []
    
    # Get all budgets
    cursor.execute(
        "SELECT * FROM budget_plans WHERE user_id = ?",
        (user_id,)
    )
    budgets = [dict(row) for row in cursor.fetchall()]
    
    # Get user preferences
    cursor.execute(
        "SELECT * FROM user_preferences WHERE user_id = ?",
        (user_id,)
    )
    preferences = dict(cursor.fetchone()) if cursor.fetchone() else {}
    
    conn.close()
    
    backup_data = {
        "backup_date": datetime.now().isoformat(),
        "version": "1.0",
        "user_id": user_id,
        "expenses": expenses,
        "income": income,
        "budgets": budgets,
        "preferences": preferences
    }
    
    return backup_data

def export_backup_json(user_id: int) -> bytes:
    """
    Export complete backup as JSON
    """
    backup_data = create_full_backup(user_id)
    return json.dumps(backup_data, indent=2, default=str).encode('utf-8')

def restore_from_backup(user_id: int, backup_json: str) -> dict:
    """
    Restore data from backup JSON
    WARNING: This will add to existing data, not replace
    """
    try:
        backup_data = json.loads(backup_json)
        
        from models.expense import add_expense
        from models.income import add_income
        from models.budget import set_budget
        
        restored = {"expenses": 0, "income": 0, "budgets": 0}
        
        # Restore expenses
        for exp in backup_data.get('expenses', []):
            result = add_expense(
                user_id,
                exp['category'],
                exp['subcategory'],
                float(exp['amount']),
                datetime.fromisoformat(exp['expense_date']).date(),
                exp.get('description', ''),
                exp.get('tags', '')
            )
            if result['success']:
                restored['expenses'] += 1
        
        # Restore income
        for inc in backup_data.get('income', []):
            result = add_income(
                user_id,
                inc['source'],
                float(inc['amount']),
                datetime.fromisoformat(inc['income_date']).date(),
                inc.get('description', '')
            )
            if result['success']:
                restored['income'] += 1
        
        # Restore budgets
        for budget in backup_data.get('budgets', []):
            result = set_budget(
                user_id,
                budget['category'],
                budget['subcategory'],
                float(budget['planned_amount']),
                int(budget['month']),
                int(budget['year'])
            )
            if result['success']:
                restored['budgets'] += 1
        
        return {
            "success": True,
            "message": f"Restored {restored['expenses']} expenses, {restored['income']} income entries, {restored['budgets']} budgets",
            "details": restored
        }
    
    except Exception as e:
        return {"success": False, "message": f"Error restoring backup: {str(e)}"}

