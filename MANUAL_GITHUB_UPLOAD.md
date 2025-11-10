# Manual GitHub Upload Guide

## Step-by-Step: Upload Files to GitHub via Web Interface

---

## Step 1: Create Repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name**: `Anadventures`
3. **Description**: "Portfolio website by Ananya Solanki"
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README" (we'll upload our own files)
6. Click **"Create repository"**

---

## Step 2: Upload Files Using GitHub Web Interface

### Option A: Upload Individual Files (Small Projects)

1. After creating the repository, you'll see an empty repository page
2. Click **"uploading an existing file"** link (or the **"Add file"** dropdown → **"Upload files"**)
3. Drag and drop your files/folders OR click **"choose your files"**
4. Upload these folders/files:
   - `app.py`
   - `wsgi.py`
   - `init_db.py`
   - `requirements.txt`
   - `runtime.txt`
   - `Procfile`
   - `README.md`
   - `LICENSE`
   - `.gitignore` (make sure to show hidden files)
   - `templates/` folder (all HTML files)
   - `static/` folder (all images and assets)
   - `data-mining/` folder (optional, but recommended)
   - All `.md` documentation files

5. Scroll down, add commit message: **"Initial commit: Anadventures portfolio"**
6. Click **"Commit changes"**

### Option B: Upload via GitHub Desktop (Easier for Large Projects)

1. Download **GitHub Desktop**: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Click **"File"** → **"Add Local Repository"**
4. Browse to: `/Users/ayushmalik/Desktop/Anadventures`
5. Click **"Publish repository"**
6. Name: `Anadventures`
7. Click **"Publish Repository"**

---

## Step 3: Important Files to Upload

### ✅ Must Upload:
- `app.py` - Main application
- `wsgi.py` - Production entry point
- `init_db.py` - Database initialization
- `requirements.txt` - Dependencies
- `runtime.txt` - Python version
- `Procfile` - Deployment config
- `README.md` - Documentation
- `.gitignore` - Git ignore rules
- `templates/` - All HTML templates
- `static/` - All static files (images, CSS, JS)
- All `.md` files (documentation)

### ❌ Do NOT Upload:
- `config.py` - Contains API keys (sensitive)
- `instance/` - Database files
- `__pycache__/` - Python cache
- `.env` - Environment variables
- `*.pkl` - Data files (optional, but large)

---

## Step 4: Upload Process

### Using Web Interface (File by File):

1. **Go to your repository**: https://github.com/anadventures/Anadventures
2. Click **"Add file"** → **"Upload files"**
3. **Drag and drop** your entire project folder OR select files
4. **Commit message**: "Initial commit: Anadventures portfolio ready for deployment"
5. Click **"Commit changes"**

### Uploading Folders:

GitHub web interface doesn't support folder upload directly, so:

**Option 1: Upload folder contents**
- Open each folder
- Upload all files inside

**Option 2: Use GitHub Desktop** (Recommended)
- Much easier for folders
- Download: https://desktop.github.com/

**Option 3: Use Git commands** (Fastest)
```bash
cd /Users/ayushmalik/Desktop/Anadventures
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## Step 5: Verify Upload

After uploading, check:
- ✅ All files are visible on GitHub
- ✅ `config.py` is NOT uploaded (it's in `.gitignore`)
- ✅ Folder structure is correct
- ✅ README.md displays properly

---

## Quick Method: GitHub Desktop (Easiest!)

### Download and Install:
1. Go to **https://desktop.github.com/**
2. Download **GitHub Desktop** for Mac
3. Install and sign in

### Upload Your Project:
1. Open **GitHub Desktop**
2. Click **"File"** → **"Add Local Repository"**
3. Click **"Choose"** and select: `/Users/ayushmalik/Desktop/Anadventures`
4. Click **"Publish repository"** button
5. Name: `Anadventures`
6. Description: "Portfolio website by Ananya Solanki"
7. Uncheck **"Keep this code private"** (if you want it public)
8. Click **"Publish Repository"**

**Done!** Your code is now on GitHub! 🎉

---

## After Upload: Deploy to Render

Once your code is on GitHub:
1. Go to **https://render.com**
2. Sign up/login
3. **New** → **Web Service**
4. Connect your **Anadventures** repository
5. Follow `RENDER_DEPLOYMENT.md` guide

---

## Troubleshooting

### "File too large"
- Some image files might be too large
- GitHub has a 100MB file limit
- Compress large images or use Git LFS

### "Can't upload folder"
- GitHub web interface doesn't support folder upload
- Use GitHub Desktop or Git commands instead

### "config.py is showing"
- Make sure `.gitignore` includes `config.py`
- Delete it from GitHub if accidentally uploaded
- It's a security risk if it contains API keys!

---

## Recommended: Use GitHub Desktop

**GitHub Desktop is the easiest way** to upload your entire project:
- ✅ Drag and drop entire folder
- ✅ Handles all files automatically
- ✅ No command line needed
- ✅ Visual interface

**Download**: https://desktop.github.com/

---

**Your repository will be at**: https://github.com/anadventures/Anadventures

