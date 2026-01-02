"""
Family Budget Manager - Main Application
A comprehensive personal finance management system
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

# Import modules
from config.database import init_database
from config.categories import BUDGET_CATEGORIES, CATEGORY_ICONS, get_all_categories, get_subcategories, get_income_categories
from utils.auth import register_user, login_user, get_user_info
from models.expense import add_expense, get_expenses, delete_expense, get_expenses_summary, get_monthly_trend
from models.budget import set_budget, get_budget_vs_actual, get_category_budget_summary, copy_budget_to_next_month
from models.income import add_income, get_income, get_monthly_balance, get_total_income, delete_income
from utils.data_export import export_expenses_to_csv, export_expenses_to_excel, export_backup_json, create_full_backup
from utils.visualizations import (
    create_category_pie_chart,
    create_monthly_trend_chart,
    create_budget_vs_actual_chart,
    create_income_vs_expenses_chart,
    create_subcategory_bar_chart
)
from utils.ai_predictions import (
    predict_next_month_expenses,
    detect_anomalies,
    generate_savings_recommendations
)

# Page configuration
st.set_page_config(
    page_title="Family Budget Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        color: #856404;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

def show_login_page():
    """Login/Register Page"""
    st.title("💰 Family Budget Manager")
    st.markdown("### Your Personal Finance Companion")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    result = login_user(username, password)
                    if result['success']:
                        st.session_state.user_id = result['user_id']
                        st.session_state.username = result['username']
                        st.success(result['message'])
                        st.rerun()
                    else:
                        st.error(result['message'])
    
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("register_form"):
            new_username = st.text_input("Choose Username (min 3 characters)")
            new_email = st.text_input("Email (optional)")
            new_password = st.text_input("Password (min 6 characters)", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("✅ Create Account", use_container_width=True)
            
            if submit:
                if not new_username or not new_password:
                    st.error("Username and password are required")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    result = register_user(new_username, new_password, new_email)
                    if result['success']:
                        st.success(result['message'])
                        st.balloons()
                    else:
                        st.error(result['message'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🔒 Your data is secure and encrypted</p>
            <p>Made with ❤️ using Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    """Main Dashboard"""
    user_info = get_user_info(st.session_state.user_id)
    
    # Sidebar
    with st.sidebar:
        st.title("💰 Budget Manager")
        st.markdown(f"**Welcome, {st.session_state.username}!**")
        
        # Month/Year selector
        st.markdown("---")
        st.subheader("📅 Select Period")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_month = st.selectbox(
                "Month",
                range(1, 13),
                index=datetime.now().month - 1,
                format_func=lambda x: calendar.month_name[x]
            )
        with col2:
            selected_year = st.selectbox(
                "Year",
                range(datetime.now().year - 2, datetime.now().year + 2),
                index=2
            )
        
        st.markdown("---")
        
        # Navigation
        menu_options = [
            "📊 Dashboard",
            "➕ Add Expense",
            "💵 Add Income",
            "📋 Budget Planning",
            "📈 Reports & Analytics",
            "🤖 AI Insights",
            "💾 Data Management",
            "⚙️ Settings"
        ]
        
        selected_page = st.radio("Navigation", menu_options)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    # Main content area
    if selected_page == "📊 Dashboard":
        show_dashboard_overview(st.session_state.user_id, selected_month, selected_year)
    elif selected_page == "➕ Add Expense":
        show_add_expense_page(st.session_state.user_id)
    elif selected_page == "💵 Add Income":
        show_add_income_page(st.session_state.user_id)
    elif selected_page == "📋 Budget Planning":
        show_budget_planning_page(st.session_state.user_id, selected_month, selected_year)
    elif selected_page == "📈 Reports & Analytics":
        show_reports_page(st.session_state.user_id, selected_month, selected_year)
    elif selected_page == "🤖 AI Insights":
        show_ai_insights_page(st.session_state.user_id, selected_month, selected_year)
    elif selected_page == "💾 Data Management":
        show_data_management_page(st.session_state.user_id)
    elif selected_page == "⚙️ Settings":
        show_settings_page(st.session_state.user_id)

def show_dashboard_overview(user_id, month, year):
    """Dashboard Overview Page"""
    st.title(f"📊 Dashboard - {calendar.month_name[month]} {year}")
    
    # Get monthly balance
    balance_info = get_monthly_balance(user_id, month, year)
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💵 Total Income",
            f"${balance_info['income']:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "💸 Total Expenses",
            f"${balance_info['expenses']:,.2f}",
            delta=None
        )
    
    with col3:
        balance_delta = f"${abs(balance_info['balance']):,.2f}"
        st.metric(
            "💰 Balance",
            f"${balance_info['balance']:,.2f}",
            delta=balance_delta if balance_info['balance'] >= 0 else f"-{balance_delta}",
            delta_color="normal" if balance_info['balance'] >= 0 else "inverse"
        )
    
    with col4:
        st.metric(
            "📊 Savings Rate",
            f"{balance_info['savings_rate']:.1f}%",
            delta=None
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    # Get expenses for current month
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    expenses_df = get_expenses(user_id, start_date, end_date)
    
    with col1:
        st.subheader("📊 Expenses by Category")
        if not expenses_df.empty:
            fig = create_category_pie_chart(expenses_df, "")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses recorded for this month")
    
    with col2:
        st.subheader("💰 Income vs Expenses")
        fig = create_income_vs_expenses_chart(balance_info, "")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent transactions
    st.markdown("---")
    st.subheader("📝 Recent Transactions")
    
    recent_expenses = get_expenses(user_id, limit=10)
    
    if not recent_expenses.empty:
        # Format the dataframe
        display_df = recent_expenses[['expense_date', 'category', 'subcategory', 'amount', 'description']].copy()
        display_df.columns = ['Date', 'Category', 'Subcategory', 'Amount', 'Description']
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet. Start by adding an expense!")

def show_add_expense_page(user_id):
    """Add Expense Page"""
    st.title("➕ Add New Expense")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Category selection OUTSIDE form for dynamic subcategory update
        category = st.selectbox(
            "Category",
            get_all_categories(),
            format_func=lambda x: f"{CATEGORY_ICONS.get(x, '📌')} {x}",
            key="expense_category_selector"
        )
        
        # Subcategory updates automatically when category changes
        subcategory = st.selectbox(
            "Subcategory",
            get_subcategories(category),
            key="expense_subcategory_selector"
        )
        
        st.markdown("---")
        
        # Rest of the form
        with st.form("add_expense_form"):
            col_c, col_d = st.columns(2)
            
            with col_c:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
            
            with col_d:
                expense_date = st.date_input("Date", value=date.today())
            
            description = st.text_area("Description (optional)", max_chars=200)
            tags = st.text_input("Tags (comma-separated, optional)")
            
            submit = st.form_submit_button("💾 Save Expense", use_container_width=True)
            
            if submit:
                result = add_expense(
                    user_id,
                    category,
                    subcategory,
                    amount,
                    expense_date,
                    description,
                    tags
                )
                
                if result['success']:
                    st.success(result['message'])
                    st.balloons()
                else:
                    st.error(result['message'])
    
    with col2:
        st.info("""
            **Quick Tips:**
            - Choose the appropriate category
            - Add descriptions for better tracking
            - Use tags for custom filtering
            - Record expenses as they happen
        """)

def show_add_income_page(user_id):
    """Add Income Page"""
    st.title("💵 Add Income")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("add_income_form"):
            source = st.selectbox(
                "Income Source",
                get_income_categories()
            )
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
            
            with col_b:
                income_date = st.date_input("Date", value=date.today())
            
            description = st.text_area("Description (optional)", max_chars=200)
            
            submit = st.form_submit_button("💾 Save Income", use_container_width=True)
            
            if submit:
                result = add_income(user_id, source, amount, income_date, description)
                
                if result['success']:
                    st.success(result['message'])
                    st.balloons()
                else:
                    st.error(result['message'])
    
    with col2:
        # Show total income for current month
        current_month = datetime.now().month
        current_year = datetime.now().year
        total = get_total_income(user_id, current_month, current_year)
        
        st.metric(
            f"Total Income - {calendar.month_name[current_month]}",
            f"${total:,.2f}"
        )
        
        st.markdown("---")
        
        st.info("""
            **Income Categories:**
            - 💼 Salary
            - 🎁 Bonus
            - 🏢 Freelance/Business
            - 🏠 Rental Income
            - 📈 Investments
            - 🎉 Gifts & Inheritance
            - 💰 Other Income
        """)

def show_budget_planning_page(user_id, month, year):
    """Budget Planning Page"""
    st.title(f"📋 Budget Planning - {calendar.month_name[month]} {year}")
    
    tab1, tab2, tab3 = st.tabs(["Set Budget", "Budget vs Actual", "Copy Budget"])
    
    with tab1:
        st.subheader("Set Monthly Budget")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Category selection OUTSIDE form for dynamic subcategory update
            category = st.selectbox(
                "Category",
                get_all_categories(),
                format_func=lambda x: f"{CATEGORY_ICONS.get(x, '📌')} {x}",
                key="budget_category_selector"
            )
            
            subcategory = st.selectbox(
                "Subcategory",
                get_subcategories(category),
                key="budget_subcategory_selector"
            )
            
            st.markdown("---")
            
            with st.form("set_budget_form"):
                planned_amount = st.number_input(
                    "Planned Amount ($)",
                    min_value=0.0,
                    step=10.0
                )
                
                submit = st.form_submit_button("💾 Set Budget", use_container_width=True)
                
                if submit:
                    result = set_budget(user_id, category, subcategory, planned_amount, month, year)
                    if result['success']:
                        st.success(result['message'])
                    else:
                        st.error(result['message'])
    
    with tab2:
        st.subheader("Budget vs Actual Comparison")
        
        comparison_df = get_budget_vs_actual(user_id, month, year)
        
        if not comparison_df.empty:
            # Summary metrics
            summary = get_category_budget_summary(user_id, month, year)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Planned", f"${summary['total_planned']:,.2f}")
            with col2:
                st.metric("Total Actual", f"${summary['total_actual']:,.2f}")
            with col3:
                diff = summary['total_difference']
                st.metric(
                    "Difference",
                    f"${abs(diff):,.2f}",
                    delta=f"${diff:,.2f}" if diff >= 0 else f"-${abs(diff):,.2f}",
                    delta_color="normal" if diff >= 0 else "inverse"
                )
            
            st.markdown("---")
            
            # Chart
            fig = create_budget_vs_actual_chart(comparison_df, "")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("Detailed Breakdown")
            display_df = comparison_df[['category', 'subcategory', 'planned_amount', 'actual_amount', 'difference', 'percentage', 'status']].copy()
            display_df.columns = ['Category', 'Subcategory', 'Planned', 'Actual', 'Difference', '%', 'Status']
            
            # Format currency columns
            for col in ['Planned', 'Actual', 'Difference']:
                display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No budget set for this month. Use the 'Set Budget' tab to get started.")
    
    with tab3:
        st.subheader("Copy Budget to Next Month")
        
        st.write("Quickly copy your current month's budget to the next month.")
        
        if st.button("📋 Copy to Next Month"):
            result = copy_budget_to_next_month(user_id, month, year)
            if result['success']:
                st.success(result['message'])
            else:
                st.error(result['message'])

def show_reports_page(user_id, month, year):
    """Reports & Analytics Page"""
    st.title(f"📈 Reports & Analytics")
    
    tab1, tab2 = st.tabs(["Monthly Analysis", "Trends"])
    
    with tab1:
        st.subheader(f"Monthly Analysis - {calendar.month_name[month]} {year}")
        
        # Get data
        start_date = date(year, month, 1)
        end_date = date(year, month, calendar.monthrange(year, month)[1])
        expenses_df = get_expenses(user_id, start_date, end_date)
        
        if not expenses_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("By Category")
                fig = create_category_pie_chart(expenses_df, "")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Category selection for detailed view
                selected_cat = st.selectbox(
                    "Select Category for Details",
                    expenses_df['category'].unique()
                )
                
                fig = create_subcategory_bar_chart(expenses_df, selected_cat)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Export options
            st.markdown("---")
            st.subheader("📥 Export Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = export_expenses_to_csv(user_id, start_date, end_date)
                if csv_data:
                    st.download_button(
                        "📄 Download CSV",
                        csv_data,
                        f"expenses_{month}_{year}.csv",
                        "text/csv",
                        use_container_width=True
                    )
            
            with col2:
                excel_data = export_expenses_to_excel(user_id, start_date, end_date)
                if excel_data:
                    st.download_button(
                        "📊 Download Excel",
                        excel_data,
                        f"expenses_{month}_{year}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        else:
            st.info("No expenses for this period")
    
    with tab2:
        st.subheader("6-Month Spending Trends")
        
        trend_df = get_monthly_trend(user_id, 6)
        
        if not trend_df.empty:
            fig = create_monthly_trend_chart(trend_df, "")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for trend analysis")

def show_ai_insights_page(user_id, month, year):
    """AI Insights Page"""
    st.title("🤖 AI-Powered Insights")
    
    tab1, tab2, tab3 = st.tabs(["💡 Predictions", "🔍 Anomaly Detection", "💰 Savings Recommendations"])
    
    with tab1:
        st.subheader("Next Month Expense Predictions")
        
        if st.button("🔮 Generate Predictions"):
            with st.spinner("Analyzing your spending patterns..."):
                predictions = predict_next_month_expenses(user_id)
                
                if predictions['success']:
                    st.success("Predictions generated!")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.metric(
                            "Total Predicted for Next Month",
                            f"${predictions['total_predicted']:,.2f}"
                        )
                    
                    with col2:
                        st.info(f"Analysis based on: {predictions['analysis_period']}")
                    
                    st.markdown("---")
                    st.subheader("Category Predictions")
                    
                    pred_data = []
                    for cat, pred in predictions['predictions'].items():
                        pred_data.append({
                            "Category": cat,
                            "Predicted": f"${pred['predicted_amount']:,.2f}",
                            "Historical Avg": f"${pred['historical_average']:,.2f}",
                            "Trend": pred['trend'],
                            "Confidence": f"{pred['confidence']:.1f}%"
                        })
                    
                    pred_df = pd.DataFrame(pred_data)
                    st.dataframe(pred_df, use_container_width=True, hide_index=True)
                else:
                    st.warning(predictions['message'])
    
    with tab2:
        st.subheader("Unusual Spending Detection")
        
        if st.button("🔎 Detect Anomalies"):
            with st.spinner("Scanning for unusual transactions..."):
                anomalies = detect_anomalies(user_id)
                
                if anomalies['success']:
                    if anomalies['anomalies_found'] > 0:
                        st.warning(f"⚠️ {anomalies['message']}")
                        
                        for anomaly in anomalies['anomalies']:
                            with st.expander(
                                f"🚨 {anomaly['category']} - ${anomaly['amount']:,.2f} on {anomaly['date']}"
                            ):
                                st.write(f"**Subcategory:** {anomaly['subcategory']}")
                                st.write(f"**Expected Range:** {anomaly['expected_range']}")
                                st.write(f"**Deviation:** {anomaly['deviation']}")
                                st.write(f"**Severity:** {anomaly['severity']}")
                    else:
                        st.success("✅ No unusual spending detected. Everything looks normal!")
                else:
                    st.info(anomalies['message'])
    
    with tab3:
        st.subheader("Personalized Savings Recommendations")
        
        if st.button("💡 Get Recommendations"):
            with st.spinner("Analyzing your budget and generating recommendations..."):
                recommendations = generate_savings_recommendations(user_id, month, year)
                
                if recommendations['success']:
                    st.success(f"Generated {len(recommendations['recommendations'])} recommendations!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Potential Monthly Savings",
                            f"${recommendations['total_potential_savings']:,.2f}"
                        )
                    with col2:
                        st.metric(
                            "Current Savings Rate",
                            f"{recommendations['current_savings_rate']:.1f}%"
                        )
                    
                    st.markdown("---")
                    
                    for rec in recommendations['recommendations']:
                        priority_color = {
                            "High": "🔴",
                            "Medium": "🟡",
                            "Low": "🟢"
                        }
                        
                        with st.expander(
                            f"{priority_color.get(rec['priority'], '🔵')} {rec['type']}: {rec['category']}"
                        ):
                            st.write(f"**{rec['message']}**")
                            st.write(f"💡 {rec['suggestion']}")
                            if 'potential_savings' in rec:
                                st.write(f"💰 Potential savings: ${rec['potential_savings']:,.2f}")
                else:
                    st.info(recommendations['message'])

def show_data_management_page(user_id):
    """Data Management Page"""
    st.title("💾 Data Management")
    
    tab1, tab2 = st.tabs(["📤 Export/Backup", "📥 Import/Restore"])
    
    with tab1:
        st.subheader("Export & Backup")
        
        st.write("Download all your data as a backup file")
        
        if st.button("📦 Create Full Backup"):
            with st.spinner("Creating backup..."):
                backup_data = export_backup_json(user_id)
                
                st.download_button(
                    "💾 Download Backup (JSON)",
                    backup_data,
                    f"budget_backup_{datetime.now().strftime('%Y%m%d')}.json",
                    "application/json",
                    use_container_width=True
                )
                
                st.success("✅ Backup ready for download!")
    
    with tab2:
        st.subheader("Import & Restore")
        st.warning("⚠️ Importing data will ADD to your existing data, not replace it.")
        
        uploaded_file = st.file_uploader("Choose a backup file", type=['json'])
        
        if uploaded_file is not None:
            if st.button("📥 Restore from Backup"):
                from utils.data_export import restore_from_backup
                
                backup_json = uploaded_file.read().decode('utf-8')
                result = restore_from_backup(user_id, backup_json)
                
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])

def show_settings_page(user_id):
    """Settings Page"""
    st.title("⚙️ Settings")
    
    user_info = get_user_info(user_id)
    
    st.subheader("Account Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {user_info['username']}")
        st.write(f"**Email:** {user_info.get('email', 'Not set')}")
    
    with col2:
        st.write(f"**Member since:** {user_info['created_at'][:10]}")
        st.write(f"**Last login:** {user_info.get('last_login', 'N/A')[:10] if user_info.get('last_login') else 'N/A'}")
    
    st.markdown("---")
    
    st.info("""
        **About this app:**
        - 🔒 All passwords are securely hashed
        - 💾 Data is stored locally (for now)
        - 📊 AI predictions use your historical data
        - 🎯 Budget tracking helps you save money
    """)

# Main application
def main():
    if st.session_state.user_id is None:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
