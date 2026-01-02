# 💰 Family Budget Manager

A comprehensive personal finance management system with AI-powered insights, built with Streamlit.

## ✨ Features

### Core Features
- 🔐 **Secure Authentication** - Password hashing with SHA-256
- 💸 **Expense Tracking** - Track expenses across 12 main categories with detailed subcategories
- 💵 **Income Management** - Record and track multiple income sources
- 📊 **Budget Planning** - Set monthly budgets and compare with actual spending
- 📈 **Interactive Visualizations** - Beautiful charts with Plotly
- 📥 **Data Export** - Export data to CSV, Excel, or JSON backup

### AI-Powered Features
- 🔮 **Expense Predictions** - ML-based predictions for next month's expenses
- 🔍 **Anomaly Detection** - Automatically detect unusual spending patterns
- 💡 **Savings Recommendations** - Personalized suggestions to save money
- 📊 **Trend Analysis** - Identify spending patterns over time

### Advanced Features
- 🏷️ **Custom Tags** - Tag expenses for better organization
- 🔄 **Budget Copying** - Copy budgets from one month to another
- 💾 **Full Backup/Restore** - Complete data backup and restore functionality
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 📁 Project Structure

```
family_budget_app/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Dependencies
├── README.md                       # This file
│
├── config/
│   ├── __init__.py
│   ├── database.py                 # Database setup and connection
│   └── categories.py               # Budget categories configuration
│
├── models/
│   ├── __init__.py
│   ├── expense.py                  # Expense CRUD operations
│   ├── budget.py                   # Budget management
│   └── income.py                   # Income tracking
│
├── utils/
│   ├── __init__.py
│   ├── auth.py                     # Authentication and password hashing
│   ├── data_export.py              # Data export utilities
│   ├── visualizations.py           # Chart generation with Plotly
│   └── ai_predictions.py           # ML predictions and insights
│
└── data/
    └── family_budget.db            # SQLite database (created automatically)
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd family_budget_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Create an account and start tracking your budget!

## 🌐 Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [streamlit.io](https://streamlit.io))

### Steps

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch (`main`), and main file (`app.py`)
   - Click "Deploy"

3. **Your app is live!** 🎉

### Important Notes for Deployment

⚠️ **Data Persistence**: The SQLite database will reset when the app restarts on Streamlit Cloud. 

**Solutions:**
- **Option 1**: Use the built-in Export/Backup feature to save your data locally
- **Option 2**: Upgrade to PostgreSQL (Supabase) for cloud persistence (requires minor code changes)
- **Option 3**: Use Google Sheets integration (can be added)

## 📊 Budget Categories

The app includes 12 main categories with detailed subcategories:

1. **👶 Children** - Childcare, School, Medical, etc.
2. **🎭 Entertainment** - Concerts, Cinema, Books, etc.
3. **🍕 Food** - Dining Out, Groceries, etc.
4. **🎁 Gifts and Charity** - Donations, Gifts, etc.
5. **🏠 Housing** - Utilities, Internet, Rent, etc.
6. **🛡️ Insurance** - Health, Home, Life
7. **💳 Loans** - Personal, Credit Cards, Student Loans
8. **💄 Personal Care** - Clothing, Beauty, Fitness
9. **🐾 Pets** - Food, Veterinary, Grooming
10. **💰 Savings or Investments** - Retirement, Investments
11. **📊 Taxes** - Federal, State, Local
12. **🚗 Transportation** - Fuel, Insurance, Maintenance

## 🤖 AI Features Explained

### Expense Predictions
- Analyzes your last 6 months of spending
- Uses moving averages and trend analysis
- Provides confidence scores for predictions

### Anomaly Detection
- Uses statistical z-score analysis
- Identifies transactions that deviate from your normal pattern
- Flags high, medium, and low severity anomalies

### Savings Recommendations
- Compares budget vs actual spending
- Identifies optimization opportunities
- Suggests realistic savings targets

## 🔒 Security

- **Password Hashing**: All passwords are hashed using SHA-256 with salt
- **No Plain Text Storage**: Passwords are never stored in plain text
- **Session Management**: Secure session handling with Streamlit
- **Local Data**: Data stored locally (or in your PostgreSQL instance)

## 📝 Usage Tips

1. **Set Monthly Budgets** - Start by setting realistic budgets for each category
2. **Record Expenses Daily** - Track expenses as they happen for best results
3. **Use Tags** - Add custom tags for better organization
4. **Review AI Insights** - Check predictions and recommendations monthly
5. **Export Regularly** - Download backups to prevent data loss

## 🛠️ Customization

### Adding Custom Categories
Edit `config/categories.py` to add your own categories and subcategories.

### Changing Colors
Modify `CATEGORY_COLORS` in `config/categories.py`.

### Currency
Currently uses USD ($). Can be modified in the code or added as a user preference.

## 📦 Dependencies

- `streamlit>=1.28.0` - Web framework
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `plotly>=5.17.0` - Interactive charts
- `openpyxl>=3.1.0` - Excel export
- `python-dateutil>=2.8.2` - Date utilities

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ by Gigione

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Charts powered by [Plotly](https://plotly.com)
- Inspired by real-world budgeting needs

---

**Happy Budgeting! 💰📊🎯**
