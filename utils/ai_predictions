"""
AI Predictions Module
Machine Learning for expense predictions, anomaly detection, and insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.database import get_connection

def predict_next_month_expenses(user_id: int, category: str = None) -> dict:
    """
    Predict next month's expenses based on historical data
    Uses simple moving average and trend analysis
    """
    conn = get_connection()
    
    # Get last 6 months of data
    query = """
        SELECT 
            strftime('%Y-%m', expense_date) as month,
            category,
            SUM(amount) as total_amount
        FROM expenses
        WHERE user_id = ?
        AND expense_date >= date('now', '-6 months')
    """
    params = [user_id]
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    query += " GROUP BY month, category ORDER BY month"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    if df.empty or len(df) < 3:
        return {
            "success": False,
            "message": "Not enough historical data for predictions (need at least 3 months)"
        }
    
    predictions = {}
    
    if category:
        # Single category prediction
        amounts = df['total_amount'].values
        
        # Simple moving average
        ma = np.mean(amounts[-3:])
        
        # Trend (linear regression slope)
        x = np.arange(len(amounts))
        trend = np.polyfit(x, amounts, 1)[0]
        
        # Prediction = MA + trend
        prediction = ma + trend
        
        # Confidence based on variance
        variance = np.var(amounts)
        confidence = max(0, min(100, 100 - (variance / ma * 20)))
        
        predictions[category] = {
            "predicted_amount": round(float(prediction), 2),
            "confidence": round(float(confidence), 1),
            "historical_average": round(float(ma), 2),
            "trend": "increasing" if trend > 0 else "decreasing",
            "months_analyzed": len(amounts)
        }
    else:
        # All categories
        for cat in df['category'].unique():
            cat_data = df[df['category'] == cat]['total_amount'].values
            
            if len(cat_data) >= 2:
                ma = np.mean(cat_data[-3:])
                x = np.arange(len(cat_data))
                trend = np.polyfit(x, cat_data, 1)[0]
                prediction = ma + trend
                
                variance = np.var(cat_data)
                confidence = max(0, min(100, 100 - (variance / ma * 20)))
                
                predictions[cat] = {
                    "predicted_amount": round(float(prediction), 2),
                    "confidence": round(float(confidence), 1),
                    "historical_average": round(float(ma), 2),
                    "trend": "increasing" if trend > 0 else "decreasing"
                }
    
    total_predicted = sum(p['predicted_amount'] for p in predictions.values())
    
    return {
        "success": True,
        "predictions": predictions,
        "total_predicted": round(total_predicted, 2),
        "analysis_period": "Last 6 months"
    }

def detect_anomalies(user_id: int, threshold: float = 2.0) -> dict:
    """
    Detect unusual spending patterns
    Uses statistical analysis (z-score) to identify anomalies
    """
    conn = get_connection()
    
    # Get last 3 months of expenses
    query = """
        SELECT id, category, subcategory, amount, expense_date
        FROM expenses
        WHERE user_id = ?
        AND expense_date >= date('now', '-3 months')
        ORDER BY expense_date DESC
    """
    
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    
    if df.empty:
        return {"success": False, "message": "Not enough data for anomaly detection"}
    
    anomalies = []
    
    # Group by category for analysis
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        
        if len(cat_data) < 5:  # Need at least 5 transactions
            continue
        
        amounts = cat_data['amount'].values
        mean = np.mean(amounts)
        std = np.std(amounts)
        
        if std == 0:  # All amounts are the same
            continue
        
        # Calculate z-scores
        z_scores = np.abs((amounts - mean) / std)
        
        # Find anomalies (z-score > threshold)
        for idx, z_score in enumerate(z_scores):
            if z_score > threshold:
                row = cat_data.iloc[idx]
                anomalies.append({
                    "id": int(row['id']),
                    "category": row['category'],
                    "subcategory": row['subcategory'],
                    "amount": float(row['amount']),
                    "date": str(row['expense_date']),
                    "expected_range": f"${mean - 2*std:.2f} - ${mean + 2*std:.2f}",
                    "deviation": f"{z_score:.1f} standard deviations",
                    "severity": "High" if z_score > 3 else "Medium"
                })
    
    return {
        "success": True,
        "anomalies_found": len(anomalies),
        "anomalies": sorted(anomalies, key=lambda x: x['amount'], reverse=True),
        "message": f"Found {len(anomalies)} unusual transactions"
    }

def generate_savings_recommendations(user_id: int, month: int, year: int) -> dict:
    """
    Generate AI-powered savings recommendations based on spending patterns
    """
    from models.budget import get_budget_vs_actual
    from models.income import get_monthly_balance
    
    # Get budget vs actual
    budget_comparison = get_budget_vs_actual(user_id, month, year)
    
    # Get monthly balance
    balance_info = get_monthly_balance(user_id, month, year)
    
    if budget_comparison.empty:
        return {
            "success": False,
            "message": "Set up a budget first to get personalized recommendations"
        }
    
    recommendations = []
    
    # Analyze over-budget categories
    over_budget = budget_comparison[budget_comparison['actual_amount'] > budget_comparison['planned_amount']]
    
    for _, row in over_budget.iterrows():
        overspend = row['actual_amount'] - row['planned_amount']
        percentage = (overspend / row['planned_amount']) * 100
        
        recommendations.append({
            "category": row['category'],
            "subcategory": row['subcategory'],
            "type": "Over Budget Alert",
            "priority": "High" if percentage > 50 else "Medium",
            "message": f"You're ${overspend:.2f} ({percentage:.1f}%) over budget in {row['subcategory']}",
            "suggestion": f"Try to reduce spending in {row['subcategory']} by ${overspend/2:.2f} next month",
            "potential_savings": round(overspend/2, 2)
        })
    
    # Analyze high-spending categories
    high_spenders = budget_comparison.nlargest(3, 'actual_amount')
    
    for _, row in high_spenders.iterrows():
        if row['category'] not in ['Housing', 'Insurance', 'Loans']:  # Skip essential fixed costs
            potential_saving = row['actual_amount'] * 0.15  # Suggest 15% reduction
            
            recommendations.append({
                "category": row['category'],
                "subcategory": row['subcategory'],
                "type": "Optimization Opportunity",
                "priority": "Medium",
                "message": f"{row['subcategory']} is one of your highest expenses (${row['actual_amount']:.2f})",
                "suggestion": f"Consider reducing by 15% to save ${potential_saving:.2f}",
                "potential_savings": round(potential_saving, 2)
            })
    
    # Overall savings rate analysis
    if balance_info['savings_rate'] < 10:
        recommendations.append({
            "category": "Overall Budget",
            "subcategory": "Savings Rate",
            "type": "Savings Goal",
            "priority": "High",
            "message": f"Your current savings rate is {balance_info['savings_rate']:.1f}%",
            "suggestion": "Aim for at least 10-20% savings rate for financial health",
            "potential_savings": balance_info['income'] * 0.1 - (balance_info['income'] - balance_info['expenses'])
        })
    
    total_potential_savings = sum(r.get('potential_savings', 0) for r in recommendations)
    
    return {
        "success": True,
        "recommendations": recommendations,
        "total_potential_savings": round(total_potential_savings, 2),
        "current_savings_rate": balance_info['savings_rate'],
        "analysis_date": datetime.now().strftime("%Y-%m-%d")
    }

def categorize_expense_auto(description: str, amount: float) -> dict:
    """
    Auto-categorize expense based on description and amount
    Uses simple keyword matching (can be enhanced with ML model)
    """
    from config.categories import BUDGET_CATEGORIES
    
    description_lower = description.lower()
    
    # Keyword mapping (simplified - can be enhanced with ML)
    keyword_mapping = {
        "Children": ["school", "tuition", "childcare", "toy", "kids", "baby"],
        "Entertainment": ["movie", "cinema", "concert", "game", "music", "book", "netflix"],
        "Food": ["restaurant", "grocery", "food", "pizza", "lunch", "dinner", "breakfast"],
        "Housing": ["rent", "electricity", "gas", "water", "internet", "phone"],
        "Transportation": ["uber", "taxi", "gas", "fuel", "parking", "metro"],
        "Personal Care": ["salon", "gym", "fitness", "beauty", "clothing"],
        "Pets": ["vet", "pet", "dog", "cat"],
        "Insurance": ["insurance"],
        "Loans": ["loan", "credit card", "debt"]
    }
    
    # Find matching category
    for category, keywords in keyword_mapping.items():
        if any(keyword in description_lower for keyword in keywords):
            # Get first subcategory as default
            subcategory = BUDGET_CATEGORIES[category][0]
            return {
                "category": category,
                "subcategory": subcategory,
                "confidence": 0.7
            }
    
    # Default to most common category
    return {
        "category": "Food",
        "subcategory": "Groceries",
        "confidence": 0.3
    }

