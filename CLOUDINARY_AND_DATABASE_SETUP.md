# Cloudinary + PostgreSQL Setup for Persistent Glimpses

## Current Setup

✅ **Cloudinary** - Already configured for images and PDFs
- Images upload to Cloudinary (persistent)
- PDFs upload to Cloudinary (persistent)
- URLs stored in database

❌ **Database** - Currently using SQLite (ephemeral on Render)
- Post metadata (title, content, category) stored in SQLite
- SQLite file gets wiped on Render restarts
- **This is why glimpses disappear!**

---

## The Fix: PostgreSQL

You need **PostgreSQL** to store post metadata permanently.

### What Gets Stored Where:

| Data Type | Storage Location | Status |
|-----------|------------------|--------|
| Images | Cloudinary | ✅ Persistent |
| PDFs | Cloudinary | ✅ Persistent |
| Post Title | Database | ❌ Needs PostgreSQL |
| Post Content | Database | ❌ Needs PostgreSQL |
| Post Category | Database | ❌ Needs PostgreSQL |
| Post Date | Database | ❌ Needs PostgreSQL |

---

## Quick Setup Steps

### 1. Create PostgreSQL Database on Render
- Dashboard → "New +" → "PostgreSQL"
- Name: `anadventures-db`
- Plan: Free
- Create

### 2. Get Database URL
- Click database → "Connections" section
- Copy "Internal Database URL"

### 3. Add to Web Service
- Web Service → "Environment" tab
- Add: `DATABASE_URL` = (paste URL)

### 4. Redeploy
- Manual Deploy → "Deploy latest commit"

### 5. Verify
- Check logs: Should see `✅ Using PostgreSQL database (production)`
- Create a glimpse
- Wait and refresh - should still be there!

---

## Environment Variables Needed on Render

Make sure you have these set in your Web Service:

1. **DATABASE_URL** - PostgreSQL connection string (from step 2)
2. **CLOUDINARY_CLOUD_NAME** - Your Cloudinary cloud name
3. **CLOUDINARY_API_KEY** - Your Cloudinary API key
4. **CLOUDINARY_API_SECRET** - Your Cloudinary API secret
5. **ANTHROPIC_API_KEY** - For chatbot
6. **SECRET_KEY** - Flask secret key

---

## How It Works Together

1. **You create a glimpse:**
   - Image uploads to Cloudinary → Gets URL
   - Post metadata saved to PostgreSQL database
   - Database stores: title, content, category, Cloudinary URLs

2. **Render restarts:**
   - Images still on Cloudinary ✅
   - Post data still in PostgreSQL ✅
   - Everything persists! ✅

3. **User views glimpse:**
   - Loads post data from PostgreSQL
   - Displays image from Cloudinary URL
   - Everything works! ✅

---

## Current Status

- ✅ Cloudinary configured and working
- ✅ Code supports PostgreSQL
- ⚠️ **Need to set up PostgreSQL on Render** (5 minutes)
- ⚠️ **Need to add DATABASE_URL environment variable**

Once PostgreSQL is set up, your glimpses will persist forever! 🎉

