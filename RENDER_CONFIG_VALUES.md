# Render Configuration - Fill These Values

## ✅ Already Correct:
- **Name**: `Anadventures` ✅
- **Language**: `Python 3` ✅
- **Branch**: `main` ✅
- **Region**: `Oregon (US West)` ✅
- **Instance Type**: `Free` ✅

## ⚠️ Need to Change:

### 1. Build Command
**Change from:**
```
pip install -r requirements.txt
```

**Change to:**
```
pip install -r requirements.txt && python3 init_db.py
```

### 2. Start Command
**Change from:**
```
gunicorn your_application.wsgi
```

**Change to:**
```
gunicorn wsgi:app
```

## 🔑 Environment Variables (IMPORTANT!)

Click **"Add Environment Variable"** and add these 3:

### Variable 1:
- **NAME**: `SECRET_KEY`
- **VALUE**: `a96d292ff33d2818e70d0d1e8c5b24e765c8a79498eee0c0103fd3db594cf0b0`

### Variable 2:
- **NAME**: `ANTHROPIC_API_KEY`
- **VALUE**: Get this from your local `config.py` file
  - Open: `/Users/ayushmalik/Desktop/Anadventures/config.py`
  - Copy the value after `ANTHROPIC_API_KEY = "`
  - Paste it here

### Variable 3:
- **NAME**: `FLASK_ENV`
- **VALUE**: `production`

## 📝 Step-by-Step:

1. **Update Build Command:**
   - Click in the "Build Command" field
   - Replace with: `pip install -r requirements.txt && python3 init_db.py`

2. **Update Start Command:**
   - Click in the "Start Command" field
   - Replace with: `gunicorn wsgi:app`

3. **Add Environment Variables:**
   - Click **"Add Environment Variable"**
   - Add all 3 variables above
   - Make sure to get `ANTHROPIC_API_KEY` from your local `config.py`

4. **Click "Deploy web service"** at the bottom!

---

**After clicking "Deploy web service", wait 2-5 minutes for deployment!** 🚀

