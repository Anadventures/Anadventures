#!/bin/bash
# Script to push Anadventures to GitHub
# Replace YOUR_GITHUB_USERNAME with your actual GitHub username

echo "🚀 Setting up GitHub repository for Anadventures..."

# Remove old remote if exists
git remote remove origin 2>/dev/null

# Add new remote (REPLACE YOUR_GITHUB_USERNAME with your actual username)
GITHUB_USERNAME="YOUR_GITHUB_USERNAME"  # Change this!
REPO_NAME="Anadventures"

git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git

# Rename branch to main
git branch -M main

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

echo "✅ Done! Your code is on GitHub at: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "Next step: Deploy to Render (see RENDER_DEPLOYMENT.md)"

