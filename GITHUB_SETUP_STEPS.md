# GitHub Setup Steps for Anadventures

## Your Repository Details
- **Repository Name**: `Anadventures`
- **GitHub Username**: (We need your actual GitHub username - it's lowercase, no spaces)

## Step 1: Create Repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name**: `Anadventures`
3. **Description**: "Portfolio website by Ananya Solanki"
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README" (we already have files)
6. Click **"Create repository"**

## Step 2: Update Git Remote

After creating the repository, GitHub will show you the URL. It will look like:
```
https://github.com/YOUR_USERNAME/Anadventures.git
```

Replace `YOUR_USERNAME` with your actual GitHub username (lowercase, no spaces).

## Step 3: Commands to Run

```bash
cd /Users/ayushmalik/Desktop/Anadventures

# Stage all changes
git add .

# Commit changes
git commit -m "Prepare for deployment: optimize code, add deployment files"

# Remove old remote (if exists)
git remote remove origin

# Add new remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Anadventures.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Common GitHub Username Formats

If your name is "Ananya Solanki", your GitHub username might be:
- `ananyasolanki`
- `ananya-solanki`
- `ananya-solanki-9099` (if includes numbers)
- Something else you chose

**Check your GitHub profile** to see your exact username in the URL:
- `https://github.com/YOUR_USERNAME`

## After Pushing

Once pushed, you can:
1. Deploy to Render (see `RENDER_DEPLOYMENT.md`)
2. View your code on GitHub
3. Set up automatic deployments

---

**Need help?** Share your GitHub username and I'll give you the exact commands!

