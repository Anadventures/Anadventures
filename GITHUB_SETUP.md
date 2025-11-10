# GitHub Repository Setup Guide

## Quick Start - Push to GitHub

### Step 1: Initialize Git (if not already done)
```bash
cd /Users/ayushmalik/Desktop/Anadventures
git init
```

### Step 2: Add All Files
```bash
git add .
```

### Step 3: Create Initial Commit
```bash
git commit -m "Initial commit: Anadventures portfolio ready for deployment"
```

### Step 4: Create GitHub Repository

**Option A: Via GitHub Website**
1. Go to https://github.com/new
2. Repository name: `anadventures` (or your preferred name)
3. Description: "Portfolio website by Ananya Solanki"
4. Choose Public or Private
5. **DO NOT** check "Initialize with README" (we already have one)
6. Click "Create repository"

**Option B: Via GitHub CLI** (if installed)
```bash
gh repo create anadventures --public --source=. --remote=origin --push
```

### Step 5: Connect and Push
```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/anadventures.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Verify
- Go to your GitHub repository
- Verify all files are present
- Check that `config.py` is NOT in the repository (it's in `.gitignore`)

## What Gets Pushed

### ✅ Included
- All Python code (`app.py`, `wsgi.py`, `init_db.py`)
- All templates (`templates/`)
- All static files (`static/`)
- Configuration files (`.gitignore`, `Procfile`, `runtime.txt`)
- Documentation (`README.md`, `DEPLOYMENT.md`, etc.)
- Requirements (`requirements.txt`)

### ❌ Excluded (via `.gitignore`)
- `config.py` - Contains API keys (sensitive)
- `instance/` - Database files
- `__pycache__/` - Python cache
- `.env` - Environment variables
- `*.pkl` - Data mining files
- IDE configuration files

## After Pushing to GitHub

### Next: Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign up/Login** (can use GitHub account)
3. **New → Web Service**
4. **Connect GitHub** → Select `anadventures` repository
5. **Configure:**
   - **Name**: `anadventures`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
6. **Environment Variables:**
   - `SECRET_KEY`: `python3 -c "import secrets; print(secrets.token_hex(32))"`
   - `ANTHROPIC_API_KEY`: (from your config.py - copy it)
   - `FLASK_ENV`: `production`
7. **Deploy!**

Your app will be live at: `https://anadventures.onrender.com`

## Important Security Notes

⚠️ **Before pushing:**
- ✅ Verify `config.py` is in `.gitignore`
- ✅ Check that no API keys are hardcoded in code
- ✅ All sensitive data uses environment variables

⚠️ **After pushing:**
- ✅ Never commit `config.py` with real keys
- ✅ Use environment variables in production
- ✅ Rotate API keys if accidentally committed

## Troubleshooting

### "Repository not found"
- Check repository name matches
- Verify you have access to the repository
- Check remote URL: `git remote -v`

### "Permission denied"
- Use HTTPS with personal access token, or
- Set up SSH keys for GitHub

### "config.py is in repository"
- Remove it: `git rm --cached config.py`
- Commit: `git commit -m "Remove config.py"`
- Push: `git push`

## Repository Structure on GitHub

```
anadventures/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── data-mining/
├── static/
├── templates/
├── .gitignore
├── app.py
├── DEPLOYMENT.md
├── DEPLOYMENT_CHECKLIST.md
├── init_db.py
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
└── wsgi.py
```

## Continuous Deployment

Once connected to Render/Railway:
- Every push to `main` branch automatically deploys
- Pull requests can be previewed
- Rollback available if needed

---

**Ready to deploy!** 🚀

Follow the steps above to push to GitHub, then deploy to Render for a live website.

