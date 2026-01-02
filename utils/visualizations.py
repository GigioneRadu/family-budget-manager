"""
Visualization Utilities
Create interactive charts and graphs using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.categories import CATEGORY_COLORS

def create_category_pie_chart(expenses_df: pd.DataFrame, title="Expenses by Category"):
    """
    Create a pie chart showing expenses distribution by category
    """
    if expenses_df.empty:
        return None
    
    category_totals = expenses_df.groupby('category')['amount'].sum().reset_index()
    category_totals = category_totals.sort_values('amount', ascending=False)
    
    # Map colors
    colors = [CATEGORY_COLORS.get(cat, '#95A5A6') for cat in category_totals['category']]
    
    fig = px.pie(
        category_totals,
        values='amount',
        names='category',
        title=title,
        color_discrete_sequence=colors,
        hole=0.4  # Donut chart
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        showlegend=True,
        height=500
    )
    
    return fig

def create_monthly_trend_chart(trend_df: pd.DataFrame, title="Monthly Spending Trend"):
    """
    Create a line chart showing monthly spending trend
    """
    if trend_df.empty:
        return None
    
    # Pivot data for better visualization
    pivot_df = trend_df.pivot(index='month', columns='category', values='total_amount').fillna(0)
    
    fig = go.Figure()
    
    for category in pivot_df.columns:
        color = CATEGORY_COLORS.get(category, '#95A5A6')
        fig.add_trace(go.Scatter(
            x=pivot_df.index,
            y=pivot_df[category],
            name=category,
            mode='lines+markers',
            line=dict(color=color, width=2),
            marker=dict(size=8),
            hovertemplate='<b>%{fullData.name}</b><br>Month: %{x}<br>Amount: $%{y:,.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=500,
        showlegend=True
    )
    
    return fig

def create_budget_vs_actual_chart(budget_comparison: pd.DataFrame, title="Budget vs Actual Spending"):
    """
    Create a grouped bar chart comparing budgeted vs actual spending
    """
    if budget_comparison.empty:
        return None
    
    # Group by category for cleaner visualization
    category_summary = budget_comparison.groupby('category').agg({
        'planned_amount': 'sum',
        'actual_amount': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Planned Budget',
        x=category_summary['category'],
        y=category_summary['planned_amount'],
        marker_color='lightblue',
        hovertemplate='<b>%{x}</b><br>Planned: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Actual Spending',
        x=category_summary['category'],
        y=category_summary['actual_amount'],
        marker_color='coral',
        hovertemplate='<b>%{x}</b><br>Actual: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Category",
        yaxis_title="Amount ($)",
        barmode='group',
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_subcategory_bar_chart(expenses_df: pd.DataFrame, category: str, title=None):
    """
    Create a bar chart for subcategories within a specific category
    """
    if expenses_df.empty:
        return None
    
    # Filter by category
    category_data = expenses_df[expenses_df['category'] == category]
    
    if category_data.empty:
        return None
    
    subcategory_totals = category_data.groupby('subcategory')['amount'].sum().reset_index()
    subcategory_totals = subcategory_totals.sort_values('amount', ascending=True)
    
    color = CATEGORY_COLORS.get(category, '#95A5A6')
    
    fig = px.bar(
        subcategory_totals,
        x='amount',
        y='subcategory',
        orientation='h',
        title=title or f"{category} - Breakdown by Subcategory",
        color_discrete_sequence=[color]
    )
    
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Amount: $%{x:,.2f}<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title="Amount ($)",
        yaxis_title="Subcategory",
        height=max(400, len(subcategory_totals) * 30)
    )
    
    return fig

def create_income_vs_expenses_chart(monthly_data: dict, title="Income vs Expenses"):
    """
    Create a comparison chart of income vs expenses
    """
    fig = go.Figure()
    
    categories = ['Income', 'Expenses', 'Balance']
    values = [
        monthly_data.get('income', 0),
        monthly_data.get('expenses', 0),
        monthly_data.get('balance', 0)
    ]
    colors = ['green' if v >= 0 else 'red' for v in values]
    colors[0] = 'lightgreen'  # Income always green
    colors[1] = 'lightcoral'  # Expenses always red
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f'${v:,.2f}' for v in values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title="Amount ($)",
        showlegend=False,
        height=400
    )
    
    return fig

def create_spending_heatmap(expenses_df: pd.DataFrame, title="Spending Heatmap"):
    """
    Create a heatmap showing spending patterns by category and month
    """
    if expenses_df.empty:
        return None
    
    # Add month column
    expenses_df['month'] = pd.to_datetime(expenses_df['expense_date']).dt.strftime('%Y-%m')
    
    # Create pivot table
    heatmap_data = expenses_df.pivot_table(
        values='amount',
        index='category',
        columns='month',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        hovertemplate='Category: %{y}<br>Month: %{x}<br>Amount: $%{z:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Category",
        height=max(400, len(heatmap_data) * 40)
    )
    
    return fig

