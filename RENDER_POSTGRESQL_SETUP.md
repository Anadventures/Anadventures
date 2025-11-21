# Setting Up PostgreSQL on Render for Persistent Database

## Why PostgreSQL?
Render's filesystem is **ephemeral** - SQLite files get wiped on each deployment. PostgreSQL is a persistent database that survives deployments.

## Step-by-Step Setup

### 1. Create PostgreSQL Database on Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `anadventures-db` (or any name you prefer)
   - **Database**: `anadventures` (or any name)
   - **User**: `anadventures_user` (or any name)
   - **Region**: Same as your web service (e.g., `Oregon (US West)`)
   - **PostgreSQL Version**: `16` (or latest)
   - **Plan**: `Free` (for testing) or `Starter` (for production)
4. Click **"Create Database"**
5. Wait 2-3 minutes for database to be created

### 2. Get Database Connection String

1. Once created, click on your PostgreSQL database
2. Find the **"Connections"** section
3. Copy the **"Internal Database URL"** (for services in same region)
   - Format: `postgresql://user:password@host:port/dbname`
4. **OR** use **"External Database URL"** if needed

### 3. Add DATABASE_URL to Your Web Service

1. Go to your **Web Service** (not the database)
2. Click on **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the database URL you copied
5. Click **"Save Changes"**

### 4. Redeploy Your Web Service

1. Go to **"Manual Deploy"** tab
2. Click **"Deploy latest commit"**
3. Wait for deployment to complete

### 5. Initialize Database Tables

After deployment, the database tables will be created automatically on first request (we added `db.create_all()` in the code).

**OR** manually initialize via Render Shell:
1. Go to your Web Service
2. Click **"Shell"** tab
3. Run: `python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"`

## Verification

1. Create a glimpse/post on your website
2. Refresh the page - it should still be there!
3. Check Render logs - you should see: `✅ Using PostgreSQL database (production)`

## Important Notes

- ✅ **Database persists** across deployments
- ✅ **Data survives** restarts and updates
- ✅ **Free tier** available (with limitations)
- ⚠️ **Backup regularly** - Free tier doesn't include automatic backups
- ⚠️ **Connection limits** - Free tier has connection limits

## Troubleshooting

### "No module named 'psycopg2'"
- Make sure `psycopg2-binary>=2.9.0` is in `requirements.txt`
- Redeploy your service

### "Connection refused"
- Check DATABASE_URL is correct
- Ensure database and web service are in same region
- Use "Internal Database URL" not "External"

### "Database does not exist"
- Make sure database name in URL matches the database you created
- Check database is running (green status)

## Migration from SQLite (Optional)

If you have existing data in SQLite:
1. Export data from SQLite
2. Import to PostgreSQL
3. Or start fresh (recommended for new deployments)

---

**That's it!** Your glimpses will now persist across deployments! 🎉

