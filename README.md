# Anadventures - by Ananya Solanki

A modern portfolio website showcasing Ananya Solanki's professional journey, creative work, and personal updates. Built with Flask and featuring an AI chatbot counterpart.

## About

Anadventures is a comprehensive portfolio website that combines professional experience, education, projects, blog posts, visual glimpses, and an AI chatbot named Ms. Matterhorn - Ananya's AI counterpart.

## Features

### 🎯 Portfolio Pages
- **Home**: Hero section, about me, latest blog posts, subscription form, and analytics dashboard
- **Experience**: Detailed professional experience with IDORI, Ogrelogic, and Boston University Consulting Group
- **Education**: Academic background from Delhi University and Boston University
- **Projects**: Key strategy projects including Market Expansion Strategy and Retention Analytics Dashboard

### 📸 Glimpses - by Ana
- Pinterest-style masonry layout for visual blog posts
- Share, download image, and download as PDF features
- Beautiful hover effects and responsive design

### ✍️ Blog
- Traditional blog layout for written content
- Categories: Work, Life, Projects, Thoughts, Updates
- Individual post pages with full content

### 🤖 Ms. Matterhorn - AI Chatbot
- AI counterpart powered by Claude 3.5 Sonnet
- Replicates Ananya's personality: optimistic, encouraging, uses pop culture references
- Modern chat interface with real-time messaging

### 📊 Analytics Dashboard
- Track views, shares, downloads, PDF downloads, subscribers, and posts
- Real-time updates (refreshes every 30 seconds)
- Only visible when logged in

### 🎂 Special Features
- Birthday popup on November 9th
- Email subscription system
- PDF generation with vintage manuscript style

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy
- **AI**: Anthropic Claude API
- **Frontend**: Bootstrap 4, HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab
- **Image Processing**: Pillow

## Dependencies

```
Flask
Flask-SQLAlchemy
Pillow
pandas
numpy
scikit-learn
reportlab
anthropic
gunicorn
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API key:
   - Edit `config.py` and add your Anthropic API key
   - Or set `ANTHROPIC_API_KEY` environment variable

3. Initialize database:
```bash
python3 init_db.py
```

4. Run the application:
```bash
python3 app.py
```

5. Visit `http://localhost:8000`

## Login Credentials

- **Username**: `anamatterhorn`
- **Password**: `manifesting_majestic_moments`

## Project Structure

```
Anadventures/
├── app.py                 # Main Flask application
├── config.py              # Configuration (API keys)
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── experience.html
│   ├── education.html
│   ├── projects.html
│   ├── glimpses.html
│   ├── blog.html
│   ├── chatbot.html
│   └── ...
├── static/                # Static files (images, CSS, JS)
└── user-data.sqlite3      # Database file
```

## Features in Detail

### Glimpses Page
- Pinterest-style card layout
- Each post can be shared, downloaded as image, or exported as PDF
- Hover effects reveal action buttons
- Responsive masonry grid

### AI Chatbot (Ms. Matterhorn)
- Powered by Claude 3.5 Sonnet
- System prompt designed to replicate Ananya's personality
- Optimistic, encouraging, uses Indian-English and American expressions
- References pop culture and Hollywood quotes
- Background: Born in Janakpuri, Delhi → Grew up in Delhi → Moved to USA for Masters

### Analytics
- Tracks all user interactions
- Views, shares, downloads, PDF downloads
- Subscriber count
- Total posts count
- Auto-refreshes every 30 seconds

## License

Copyright © 2024 Ananya Solanki. All rights reserved.

## Deployment

⚠️ **Important**: This is a Flask application and **cannot be deployed to GitHub Pages** (which only supports static sites).

### Recommended Deployment Platforms

For free deployment, use one of these platforms that support Flask:

1. **Render** (Recommended) - https://render.com
   - Free tier available
   - Easy GitHub integration
   - See `DEPLOYMENT.md` for detailed instructions

2. **Railway** - https://railway.app
   - Free tier with $5 monthly credit
   - Simple deployment

3. **Fly.io** - https://fly.io
   - Free tier available

### Quick Deploy Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/anadventures.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Sign up at https://render.com
   - New → Web Service → Connect GitHub
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Add environment variables:
     - `SECRET_KEY` (generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"`)
     - `ANTHROPIC_API_KEY` (your API key)
     - `FLASK_ENV=production`

3. **Initialize database** (after first deployment):
   - Use Render's shell or add to build command

See `DEPLOYMENT.md` for complete deployment guide.

## Environment Variables

For production, set these environment variables:

- `SECRET_KEY`: Random secret key for Flask sessions
- `ANTHROPIC_API_KEY`: Your Anthropic API key for chatbot
- `FLASK_ENV`: Set to `production` for production
- `PORT`: Usually auto-set by hosting platform

## Contact

- **Email**: ananyasolanki9099@gmail.com
- **Phone**: 857-869-8321
- **Website**: Anadventures - by Ananya Solanki
