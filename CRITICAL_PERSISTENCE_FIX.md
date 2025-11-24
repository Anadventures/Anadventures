# 🚨 CRITICAL: Fix Glimpses Persistence on Render

## The Problem
Your glimpses are disappearing when Render restarts because **SQLite files are stored in the filesystem, which is ephemeral on Render**. Every time Render restarts or redeploys, the SQLite database file gets wiped.

## The Solution: PostgreSQL
You **MUST** set up PostgreSQL on Render for glimpses to persist permanently.

---

## ⚡ QUICK FIX (5 Minutes)

### Step 1: Create PostgreSQL Database
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `anadventures-db`
   - **Database**: `anadventures`
   - **User**: `anadventures_user`
   - **Region**: Same as your web service
   - **Plan**: **Free** (for now)
4. Click **"Create Database"**
5. Wait 2-3 minutes

### Step 2: Get Database URL
1. Click on your PostgreSQL database
2. Scroll to **"Connections"** section
3. Copy **"Internal Database URL"**
   - Looks like: `postgresql://user:pass@host:port/dbname`

### Step 3: Add to Web Service
1. Go to your **Web Service** (not the database)
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: (paste the URL you copied)
5. Click **"Save Changes"**

### Step 4: Redeploy
1. Go to **"Manual Deploy"** tab
2. Click **"Deploy latest commit"**
3. Wait for deployment

### Step 5: Verify
1. Check logs - should see: `✅ Using PostgreSQL database (production)`
2. Create a glimpse
3. Wait a few minutes, then refresh
4. **Glimpse should still be there!** ✅

---

## ✅ What I've Already Done

- ✅ Code automatically detects PostgreSQL
- ✅ Database tables created on startup
- ✅ Works with both SQLite (local) and PostgreSQL (Render)
- ✅ All your glimpses will be saved to PostgreSQL

---

## 🔍 How to Verify It's Working

After setting up PostgreSQL, check your Render logs. You should see:
```
✅ Using PostgreSQL database (production)
✅ Database tables verified/created on startup
```

If you see:
```
✅ Using SQLite database (development)
```
Then PostgreSQL is NOT set up yet - follow the steps above!

---

## 📝 Important Notes

- **Free PostgreSQL tier** has limitations but works for small-medium traffic
- **Data persists** across deployments, restarts, and updates
- **No data loss** once PostgreSQL is configured
- **Automatic backups** available on paid tiers

---

## 🆘 Still Having Issues?

1. **Check DATABASE_URL** is set correctly in environment variables
2. **Check database and web service** are in same region
3. **Check logs** for database connection errors
4. **Verify PostgreSQL** is running (green status)

---

**Once PostgreSQL is set up, your glimpses will persist forever!** 🎉

