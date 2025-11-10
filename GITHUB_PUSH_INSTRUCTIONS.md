# GitHub Push Instructions

## ✅ Repository Setup Complete!

Your local repository is now configured to push to:
**https://github.com/anadventures/Anadventures.git**

## ⚠️ Authentication Required

To push to GitHub, you need to authenticate. Here are your options:

---

## Option 1: Personal Access Token (Recommended)

### Step 1: Create Personal Access Token
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **"Generate new token (classic)"**
3. Give it a name: "Anadventures Deployment"
4. Select scopes: Check **"repo"** (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

### Step 2: Push Using Token
```bash
cd /Users/ayushmalik/Desktop/Anadventures
git push -u origin main
```

When prompted:
- **Username**: `anadventures`
- **Password**: Paste your personal access token (not your GitHub password)

---

## Option 2: SSH Keys (Alternative)

### Step 1: Check if you have SSH key
```bash
ls -al ~/.ssh
```

### Step 2: Generate SSH key (if needed)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### Step 3: Add to GitHub
1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste your key and save

### Step 4: Change remote to SSH
```bash
cd /Users/ayushmalik/Desktop/Anadventures
git remote set-url origin git@github.com:anadventures/Anadventures.git
git push -u origin main
```

---

## Option 3: GitHub CLI (Easiest)

### Install GitHub CLI
```bash
brew install gh
```

### Authenticate
```bash
gh auth login
```

### Push
```bash
cd /Users/ayushmalik/Desktop/Anadventures
git push -u origin main
```

---

## ⚠️ Important: Create Repository First!

**Before pushing, make sure the repository exists on GitHub:**

1. Go to **https://github.com/new**
2. Repository name: `Anadventures`
3. **DO NOT** initialize with README
4. Click **"Create repository"**

---

## Quick Push Command

Once authenticated, just run:
```bash
cd /Users/ayushmalik/Desktop/Anadventures
git push -u origin main
```

---

## Verify After Push

After successful push, visit:
**https://github.com/anadventures/Anadventures**

You should see all your files there!

---

## Next Step: Deploy to Render

Once code is on GitHub:
1. Go to https://render.com
2. Connect your GitHub account
3. Deploy (see `RENDER_DEPLOYMENT.md`)

