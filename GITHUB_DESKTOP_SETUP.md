# GitHub Desktop Setup - Step by Step

## Step 1: Download GitHub Desktop

I've opened the download page for you. If it didn't open, go to:
**https://desktop.github.com/**

1. Click the big **"Download for macOS"** button
2. The download will start automatically
3. Wait for the `.zip` file to download (usually in your Downloads folder)

## Step 2: Install GitHub Desktop

1. Go to your **Downloads** folder
2. Find `GitHubDesktop.zip` (or similar name)
3. **Double-click** to extract it
4. You'll see `GitHub Desktop.app`
5. **Drag** `GitHub Desktop.app` to your **Applications** folder
6. Open **Applications** folder and **double-click** `GitHub Desktop.app`
7. If you see a security warning, go to:
   - **System Settings** → **Privacy & Security**
   - Click **"Open Anyway"** next to the GitHub Desktop message

## Step 3: Sign In to GitHub

1. GitHub Desktop will open
2. Click **"Sign in to GitHub.com"**
3. Enter your credentials:
   - **Username**: `anadventures`
   - **Password**: Your GitHub password
4. Authorize GitHub Desktop
5. You're signed in! ✅

## Step 4: Add Your Project

1. In GitHub Desktop, click **"File"** → **"Add Local Repository"**
2. Click **"Choose"** button
3. Navigate to: `/Users/ayushmalik/Desktop/Anadventures`
4. Select the **Anadventures** folder
5. Click **"Add Repository"**

## Step 5: Publish to GitHub

1. You'll see all your files listed in GitHub Desktop
2. At the top, you'll see: **"Publish repository"** button
3. Click **"Publish repository"**
4. In the popup:
   - **Name**: `Anadventures` (should be pre-filled)
   - **Description**: "Portfolio website by Ananya Solanki"
   - **Keep this code private**: Uncheck if you want it public
5. Click **"Publish Repository"**

## Step 6: Verify

1. GitHub Desktop will show "Published" ✅
2. Go to: **https://github.com/anadventures/Anadventures**
3. You should see all your files there!

---

## Troubleshooting

### "Can't find the folder"
- Make sure you're selecting `/Users/ayushmalik/Desktop/Anadventures`
- The folder should contain `app.py`, `templates/`, `static/`, etc.

### "Repository already exists"
- The repository might already exist on GitHub
- In GitHub Desktop, click **"Repository"** → **"Repository Settings"** → **"Remote"**
- Make sure it points to: `https://github.com/anadventures/Anadventures.git`

### "Authentication failed"
- Make sure you're signed in with username: `anadventures`
- Check your GitHub password
- You might need to create a Personal Access Token

---

## After Publishing

Once your code is on GitHub:
1. ✅ Your repository: https://github.com/anadventures/Anadventures
2. ✅ Next step: Deploy to Render (see `RENDER_DEPLOYMENT.md`)

---

**Need help?** Let me know if you get stuck at any step!

