# 🚀 Deployment Guide - Streamlit Cloud

This guide will walk you through deploying your Family Budget Manager to Streamlit Cloud.

## Prerequisites

✅ GitHub account  
✅ Streamlit Cloud account (free at https://streamlit.io)  
✅ Your code ready in the `family_budget_app` folder

## Step-by-Step Deployment

### 1. Create GitHub Repository

1. Go to https://github.com and sign in
2. Click the **"+"** button → **"New repository"**
3. Name it: `family-budget-manager` (or any name you prefer)
4. Make it **Public** or **Private** (both work)
5. Do NOT initialize with README (we already have one)
6. Click **"Create repository"**

### 2. Push Your Code to GitHub

Open your terminal in the `family_budget_app` directory and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Family Budget Manager"

# Add your GitHub repo as remote (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/family-budget-manager.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

### 3. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in the deployment form:
   - **Repository**: Select `YOUR_USERNAME/family-budget-manager`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain
5. Click **"Deploy!"**

### 4. Wait for Deployment

- Streamlit Cloud will:
  - Install dependencies from `requirements.txt`
  - Initialize your app
  - Create a public URL

- This usually takes 2-3 minutes ⏱️

### 5. Your App is Live! 🎉

You'll get a URL like: `https://your-app-name.streamlit.app`

Share it with anyone, and they can start tracking their budget!

## ⚠️ Important Notes

### Data Persistence

**SQLite limitation on Streamlit Cloud:**
- The database file (`data/family_budget.db`) will reset when the app restarts
- App restarts happen when you push code updates or after periods of inactivity

**Solutions:**

#### Option 1: Manual Backup (Built-in)
- Use the "Data Management" page in the app
- Click "Create Full Backup" to download your data as JSON
- Import it back later using "Import & Restore"

#### Option 2: PostgreSQL with Supabase (Recommended for Production)

1. Create free account at https://supabase.com
2. Create a new project
3. Get your connection string
4. In Streamlit Cloud, go to app settings → Secrets
5. Add your database URL:
   ```toml
   DATABASE_URL = "postgresql://..."
   ```
6. Modify `config/database.py` to use PostgreSQL when `DATABASE_URL` is set

#### Option 3: Google Sheets Integration
- Can be added as a data persistence layer
- Requires Google Sheets API setup
- Good for collaborative budgets

### Security Best Practices

1. **Never commit sensitive data** to GitHub
2. **Use Streamlit Secrets** for API keys and credentials
3. **Enable 2FA** on your GitHub account
4. **Review access** to your Streamlit Cloud apps regularly

### Managing Updates

To update your deployed app:

```bash
# Make changes to your code
# Then commit and push

git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically redeploy with your changes!

### Monitoring Your App

In Streamlit Cloud dashboard, you can:
- 📊 View app metrics and usage
- 📝 Check logs for errors
- ⚙️ Manage settings
- 🔄 Manually reboot the app
- ❌ Delete the app

## 🎯 Next Steps

After deployment:

1. **Test the app** - Create an account and test all features
2. **Share the URL** - Give it to family/friends
3. **Monitor usage** - Check Streamlit Cloud dashboard
4. **Consider upgrades**:
   - Add PostgreSQL for data persistence
   - Add email notifications
   - Add mobile app (with Streamlit in Snowflake)
   - Add multi-currency support

## 🆘 Troubleshooting

### App won't start
- Check Streamlit Cloud logs for errors
- Verify `requirements.txt` has all dependencies
- Make sure `app.py` is in the root directory

### Missing dependencies
Add them to `requirements.txt`:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### Database errors
- SQLite has limited write concurrency
- Consider upgrading to PostgreSQL for multiple users

### Performance issues
- Streamlit Cloud free tier has resource limits
- Use `@st.cache_data` for expensive computations
- Optimize database queries

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **GitHub Issues**: Create issues in your repo

---

**Happy Deploying! 🚀**
