# Deployment Guide for Anadventures

## ⚠️ Important: GitHub Pages Limitation

**GitHub Pages cannot host Flask applications.** GitHub Pages only supports static websites (HTML, CSS, JavaScript). Since Anadventures is a Flask application with:
- Backend server (Python/Flask)
- Database (SQLite)
- API endpoints (/api/chat)
- Server-side sessions
- File uploads

You need a platform that supports Python/Flask applications.

## Recommended Free Deployment Platforms

### 1. **Render** (Recommended - Easiest)
- **Free tier**: Yes (with limitations)
- **Setup**: Very easy, connects to GitHub
- **URL**: https://render.com

**Steps:**
1. Push your code to GitHub
2. Go to Render.com and sign up
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Environment Variables**:
     - `SECRET_KEY`: Generate a random secret key
     - `ANTHROPIC_API_KEY`: Your Anthropic API key
     - `FLASK_ENV`: `production`
6. Deploy!

### 2. **Railway**
- **Free tier**: Yes (with $5 credit monthly)
- **Setup**: Easy, connects to GitHub
- **URL**: https://railway.app

**Steps:**
1. Push code to GitHub
2. Go to Railway.app and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables in the Variables tab
6. Railway auto-detects Flask and deploys!

### 3. **Fly.io**
- **Free tier**: Yes
- **Setup**: Medium difficulty
- **URL**: https://fly.io

### 4. **Heroku** (Paid now, but has alternatives)
- Heroku removed free tier, but alternatives exist

## Pre-Deployment Checklist

✅ **Code is ready:**
- [x] `.gitignore` created (excludes sensitive files)
- [x] Security fixes applied (secret key uses env vars)
- [x] Unused imports removed
- [x] Code bugs fixed
- [x] `wsgi.py` configured for production
- [x] `Procfile` exists for Heroku/Render
- [x] `requirements.txt` is complete

## Environment Variables to Set

Before deploying, you'll need to set these environment variables on your hosting platform:

```bash
SECRET_KEY=your-random-secret-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key
FLASK_ENV=production
PORT=8000  # Usually auto-set by platform
```

### Generate a Secret Key:
```python
import secrets
print(secrets.token_hex(32))
```

## Database Initialization

After deployment, you may need to initialize the database. Most platforms allow you to run commands:

```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

Or add this to your deployment startup script.

## Post-Deployment Steps

1. **Test all features:**
   - Home page loads
   - Blog posts display
   - Chatbot works (check API key)
   - Login works
   - File uploads work (if applicable)

2. **Set up custom domain** (optional):
   - Most platforms allow custom domains
   - Update DNS settings

3. **Monitor logs:**
   - Check platform logs for errors
   - Monitor API usage

## Troubleshooting

### Database Issues
- Ensure `instance/` folder is writable
- Check database path permissions

### API Key Issues
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check API key has sufficient credits

### Static Files Not Loading
- Ensure `static/` folder is in repository
- Check file paths are relative

### Port Issues
- Most platforms set `PORT` automatically
- Don't hardcode port numbers

## Alternative: Static Site Conversion

If you absolutely must use GitHub Pages, you would need to:
1. Convert Flask app to static HTML
2. Use client-side JavaScript for dynamic features
3. Use external APIs for backend functionality
4. **This would require significant refactoring and lose many features**

**Not recommended** - Use a Flask-compatible platform instead.

## Quick Start with Render

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/anadventures.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/login
   - New → Web Service
   - Connect GitHub repo
   - Use these settings:
     - **Name**: anadventures
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn wsgi:app`
   - Add environment variables
   - Deploy!

Your app will be live at: `https://anadventures.onrender.com` (or your custom domain)

---

**Need help?** Check platform-specific documentation or contact support.

