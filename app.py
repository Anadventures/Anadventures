import os
import re
from flask import Flask, render_template, session, request, redirect, send_from_directory, jsonify, make_response
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import random
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
import pickle
from collections import Counter
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import io
import anthropic
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests

# Try to import config, fallback to environment variable
try:
    from config import ANTHROPIC_API_KEY as CONFIG_API_KEY
except ImportError:
    CONFIG_API_KEY = None

# Flask app configs
app=Flask(__name__)

# Database configuration - Use PostgreSQL on Render, SQLite locally
# Render provides DATABASE_URL environment variable for PostgreSQL
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Production: Use PostgreSQL from Render
    # Render's DATABASE_URL format: postgresql://user:pass@host:port/dbname
    # SQLAlchemy needs postgresql:// (not postgres://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("✅ Using PostgreSQL database (production)")
else:
    # Development: Use SQLite
    os.makedirs('instance', exist_ok=True)
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'user-data.sqlite3')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print("✅ Using SQLite database (development)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Use environment variable for secret key in production, fallback for development
app.secret_key = os.environ.get('SECRET_KEY', 'soverysecret-dev-key-change-in-production')

# Cloudinary Configuration
cloudinary.config( 
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.environ.get('CLOUDINARY_API_KEY'), 
  api_secret = os.environ.get('CLOUDINARY_API_SECRET') 
)

#Database 
db = SQLAlchemy(app)
class users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    interests = db.Column(db.String(200))

class images(db.Model):
    id = db.Column('image_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    fields = db.Column(db.String(300))
    description = db.Column(db.String(1000))
    links = db.Column(db.String(200))
    user_id  = db.Column(db.Integer)

class user_slugs(db.Model):
    id = db.Column('slug_id', db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    bio = db.Column(db.String(1000))
    website = db.Column(db.String(100))

class pin_category(db.Model):
    id = db.Column('category_id', db.Integer, primary_key=True)
    name = db.Column(db.String(200))

class track_visits(db.Model):
    id = db.Column('visit_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    img_id = db.Column(db.Integer)

class admin_post(db.Model):
    id = db.Column('admin_id', db.Integer, primary_key=True)
    advertisement_title = db.Column(db.String(100))
    thought_title = db.Column(db.String(100))
    advertisement_link = db.Column(db.String(100))
    thought_link = db.Column(db.String(100))
    date = db.Column(db.String(100))

class follow_user(db.Model):
    id = db.Column('follow_id', db.Integer, primary_key=True)
    user_email = db.Column(db.String(100))
    follower_email = db.Column(db.String(100))

class saved_pins(db.Model):
    id = db.Column('save_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    img_id = db.Column(db.Integer)

# New models for portfolio/blog
class blog_posts(db.Model):
    id = db.Column('post_id', db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    category = db.Column(db.String(100))  # Work, Life, Projects, etc.
    content = db.Column(db.Text)
    image_path = db.Column(db.String(500)) # Increased length for Cloudinary URLs
    pdf_path = db.Column(db.String(500))  # Increased length for Cloudinary URLs
    created_at = db.Column(db.String(100))
    show_date = db.Column(db.Boolean, default=True)  # Toggle to show/hide date
    author_id = db.Column(db.Integer, default=1)  # Ananya's ID

class subscribers(db.Model):
    id = db.Column('subscriber_id', db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    subscribed_at = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

class analytics(db.Model):
    id = db.Column('analytics_id', db.Integer, primary_key=True)
    event_type = db.Column(db.String(50))  # view, share, download, pdf_download, subscribe
    post_id = db.Column(db.Integer, nullable=True)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.String(100))

# Initialize database tables
# Run this once to create the database schema
def init_db():
    """Initialize the database with all tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

# Initialize database on app startup (important for Render deployment)
# This ensures tables are created when the app starts
def initialize_database():
    """Initialize database and migrate existing data if needed"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables verified/created on startup")
            
            # Migrate existing posts to add show_date field if missing
            try:
                posts = blog_posts.query.all()
                migrated = 0
                for post in posts:
                    if post.show_date is None:
                        post.show_date = True  # Default to showing date
                        migrated += 1
                if migrated > 0:
                    db.session.commit()
                    print(f"✅ Migrated {migrated} posts with show_date field")
            except Exception as e:
                print(f"⚠️ Migration note: {e}")
                db.session.rollback()
        except Exception as e:
            print(f"⚠️ Database initialization note: {e}")

# Run initialization
initialize_database()


#Data extractors 
def extract_users():
    records=users.query.all()
    id,email,interests=[],[],[]
    for rec in records:
        var_id,var_name=rec.id,rec.email
        for interest in rec.interests.split(","):
            id.append(var_id)
            email.append(var_name)
            interests.append(interest)

    df=pd.DataFrame({"user_id":pd.Series(id),"name":pd.Series(email),"category":pd.Series(interests),"flag":pd.Series(np.ones(len(email)))})
    return df

def extract_images():
    records=images.query.all()
    id,title,fields,user_ids=[],[],[],[]
    for rec in records:
        id.append(rec.id)
        title.append(rec.title)
        fields.append(rec.fields)
        user_ids.append(rec.user_id)

    df=pd.DataFrame({"img_id":pd.Series(id),"title":pd.Series(title),"category":pd.Series(fields),"user_id":pd.Series(user_ids),"img_flag":pd.Series(np.ones(len(title)))})
    return df

def extract_tracks():
    records=track_visits.query.all()
    id,user_ids,img_ids=[],[],[]
    for rec in records:
        id.append(rec.id)
        user_ids.append(rec.user_id)
        img_ids.append(rec.img_id)

    df=pd.DataFrame({"visit_id":pd.Series(id),"user_id":pd.Series(user_ids),"img_id":pd.Series(img_ids),"visits":pd.Series(np.ones(len(id)))})
    return df 

def extract_category():
    records=pin_category.query.all()
    id,name=[],[]
    for rec in records:
        id.append(rec.id)
        name.append(rec.name)

    df=pd.DataFrame({"cat_id":pd.Series(id),"category":pd.Series(name)})
    return df

#calls to compute ratings crosstab matrix and perform Pearson Correlation
#user-user similarity find out
def compute_user_similarity():
    user_data=extract_users()
    image_data=extract_images()
    track_data=extract_tracks()
    category_data=extract_category()

    #user_merge_category=pd.merge(user_data[["name","category"]],category_data[["category"]],on="category")
    user_merge_category=pd.merge(user_data[["name","category","flag"]],category_data[["category"]],on="category")
    user_category = user_merge_category.pivot_table(values='flag', index='name', columns='category', fill_value=0)
    combined_dataset=pd.merge(user_data[["user_id","name"]],image_data[["img_id","user_id","category","img_flag"]],on="user_id")
    user_images = combined_dataset.pivot_table(values= 'img_flag', index='name', columns='category', fill_value=0)
    track_images=pd.merge(image_data[['img_id','title']],track_data[['img_id','user_id']],on="img_id")
    track_user_images=pd.merge(track_images,user_data[["user_id","name"]],on="user_id")

    final_set=pd.merge(user_category,user_images,on="name")
    from sklearn.decomposition import TruncatedSVD

    #generate SVD matrix
    SVD = TruncatedSVD(n_components=5, random_state=17)
    resultant_matrix = SVD.fit_transform(final_set)
    #Computing similarity scores
    corr_mat = np.corrcoef(resultant_matrix)
    import pickle
    # save array
    with open('data-mining/user-corr.pkl','wb') as file:
        pickle.dump(corr_mat,file)
    # save track_data
    with open('data-mining/track_data.pkl','wb') as file:
        pickle.dump(track_user_images,file)
    # save final set 
    with open("data-mining/final_set.pkl",'wb') as file:
        pickle.dump(final_set,file)

#compute_user_similarity()
#Function to return images based on user-user collaborative filtering
def call(nm):
    with open('data-mining/final_set.pkl','rb') as file:
        final_set=pickle.load(file)
    with open('data-mining/user-corr.pkl','rb') as file:
        corr_mat=pickle.load(file)
    with open('data-mining/track_data.pkl','rb') as file:
        track_user_images=pickle.load(file)

    threshold=0.3
    user_list=list(final_set.index)

    idx=user_list.index(nm)
    user_select=Counter()
    
    itr=0
    for score in corr_mat[idx]:
        if score>0.98 or score<threshold:
            itr+=1
        else:
            user_select[itr]=score
            itr+=1

    #Common users
    common_users=5    #Change it to generate more data

    image_names,ids=[],[]
    for k,u in user_select.most_common(common_users):
        email=user_list[k]
        row=track_user_images[track_user_images["name"]==email]
        
        img_names=row.title.values
        id_imgs=row.img_id.values
        
        for i in range(len(img_names)):
            nm=img_names[i]
            idsers=id_imgs[i]
            if nm in image_names:
                continue 
            else:
                image_names.append(nm)
                ids.append(idsers)

    ls_objs=[]
    for var in ids:
        img_obj = images.query.filter_by(id=var).first()
        if img_obj:
            ls_objs.append(img_obj)
    return ls_objs

#Admin post 
@app.route("/admin_post",methods=["GET","POST"])
def admin_listing():
    if request.method=="GET":
        return render_template("admin_post.html",display_nm="Admin")
    else:
        advertisment_title=request.form.get('iname2')
        advertisment_link=request.form.get('link2')
        thought_title=request.form.get('iname1')
        thought_link=request.form.get('link1')
        img_path_adv=request.files['img2']
        img_path_thought=request.files['img1']

        #Creating date-string 
        dt=datetime.now()
        format=dt.strftime("%d %B, %Y")

        admin_obj=admin_post(advertisement_link=advertisment_link,advertisement_title=advertisment_title,thought_title=thought_title,thought_link=thought_link,date=format)
        db.session.add(admin_obj)
        db.session.commit()


        img1=Image.open(img_path_adv)
        img2=Image.open(img_path_thought)

        #retreive id 
        admin_rec=admin_post.query.filter_by(date=format).all()
        admin_rec=admin_rec[0]
        admin_id=admin_rec.id
        
        img1.save('static/admin_promo/adv'+str(admin_id)+".jpg")
        img2.save('static/admin_promo/thought'+str(admin_id)+".jpg")

        return redirect(url_for('index'))


# Portfolio Routing functions
@app.route('/')
def index():
    # Home/About page
    blog_posts_list = blog_posts.query.order_by(blog_posts.id.desc()).limit(6).all()
    # Get glimpses (posts with images) for carousel
    glimpses_list = blog_posts.query.filter(blog_posts.image_path.isnot(None), blog_posts.image_path != '').order_by(blog_posts.id.desc()).limit(10).all()
    track_analytics("view", None)  # Track homepage views
    # Check if it's November 9th
    today = datetime.now()
    is_birthday = today.month == 11 and today.day == 9
    return render_template("home.html", display_nm="Ananya Solanki", blog_posts=blog_posts_list, glimpses=glimpses_list, is_birthday=is_birthday)

@app.route('/experience')
def experience():
    return render_template("experience.html", display_nm="Ananya Solanki")

@app.route('/education')
def education():
    return render_template("education.html", display_nm="Ananya Solanki")

@app.route('/projects')
def projects():
    return render_template("projects.html", display_nm="Ananya Solanki")

@app.route('/glimpses')
def glimpses():
    try:
        # Ensure database tables exist
        db.create_all()
        posts = blog_posts.query.order_by(blog_posts.id.desc()).all()
        print(f"✅ Found {len(posts)} posts in database")
        # Check if user is logged in as Ananya
        is_admin = "username" in session and session.get("username") == "Ananya Solanki"
        return render_template("glimpses.html", display_nm="Ananya Solanki", posts=posts, is_admin=is_admin)
    except Exception as e:
        print(f"❌ Error loading glimpses: {e}")
        import traceback
        traceback.print_exc()
        # Return empty list on error
        is_admin = "username" in session and session.get("username") == "Ananya Solanki"
        return render_template("glimpses.html", display_nm="Ananya Solanki", posts=[], is_admin=is_admin)

@app.route('/blog')
def blog():
    posts = blog_posts.query.order_by(blog_posts.id.desc()).all()
    return render_template("blog.html", display_nm="Ananya Solanki", posts=posts)

@app.route('/blog/<post_id>')
def blog_post(post_id):
    post = blog_posts.query.filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('blog'))
    track_analytics("view", post_id)
    # Check if user is logged in as Ananya
    is_admin = "username" in session and session.get("username") == "Ananya Solanki"
    return render_template("blog_post.html", display_nm="Ananya Solanki", post=post, is_admin=is_admin)

@app.route('/glimpses/<post_id>')
def glimpse_post(post_id):
    post = blog_posts.query.filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('glimpses'))
    track_analytics("view", post_id)
    # Check if user is logged in as Ananya
    is_admin = "username" in session and session.get("username") == "Ananya Solanki"
    return render_template("glimpse_post.html", display_nm="Ananya Solanki", post=post, is_admin=is_admin)

@app.route('/share/<post_id>')
def share_post(post_id):
    track_analytics("share", post_id)
    return jsonify({"status": "success"})

@app.route('/download-image/<post_id>')
def download_image(post_id):
    post = blog_posts.query.filter_by(id=post_id).first()
    if not post or not post.image_path:
        return redirect(url_for('glimpses'))
    track_analytics("download", post_id)
    
    # If it's a Cloudinary URL, redirect to it
    if post.image_path.startswith('http'):
        return redirect(post.image_path)
        
    # Fallback for local files (legacy)
    return send_from_directory(directory=os.path.dirname(post.image_path), path=os.path.basename(post.image_path), as_attachment=True)

@app.route('/download-pdf/<post_id>')
def download_pdf(post_id):
    post = blog_posts.query.filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('glimpses'))
    
    track_analytics("pdf_download", post_id)
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch, bottomMargin=1*inch)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2c3e50',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    content_style = ParagraphStyle(
        'CustomContent',
        parent=styles['Normal'],
        fontSize=12,
        textColor='#34495e',
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=18,
        fontName='Helvetica'
    )
    
    meta_style = ParagraphStyle(
        'CustomMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#7f8c8d',
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Add title
    story.append(Paragraph(post.title, title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add metadata
    meta_text = f"<i>{post.category} • {post.created_at}</i>"
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Add image if exists
    if post.image_path:
        try:
            img_data = None
            if post.image_path.startswith('http'):
                # Download image from Cloudinary
                response = requests.get(post.image_path)
                if response.status_code == 200:
                    img_data = io.BytesIO(response.content)
            elif os.path.exists(post.image_path):
                # Local file
                img_data = post.image_path
                
            if img_data:
                img = RLImage(img_data, width=5*inch, height=5*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
        except Exception as e:
            print(f"Error adding image to PDF: {e}")
            pass
    
    # Add content
    content_lines = post.content.split('\n')
    for line in content_lines:
        if line.strip():
            story.append(Paragraph(line.strip(), content_style))
        else:
            story.append(Spacer(1, 0.1*inch))
    
    # Add footer
    story.append(Spacer(1, 0.5*inch))
    footer_text = "<i>Anadventures - by Ananya Solanki</i>"
    story.append(Paragraph(footer_text, meta_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Create response
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=glimpse_{post_id}_{post.title.replace(" ", "_")}.pdf'
    return response

@app.route('/follow/<email>',methods=["POST"])
def user_follow_action(email):
    if request.method=="GET":
        return redirect(url_for('index'))

    if "username" not in session:
        return render_template("sign.html",display_nm="Author",error="You need to log in to follow users.")

    u_email=session["email"]
    obj=follow_user(user_email=email,follower_email=u_email)
    db.session.add(obj)
    db.session.commit()

    return redirect(url_for('profile_view',profile_email=email,action=1))

@app.route('/today')
def exclusive():
    if "username" in session:
        nm=session["username"]
    else:
        nm="Author"
    
    listing_images=admin_post.query.all()[::-1]
    return render_template("latest_uploaded.html",display_nm=nm,images_list=listing_images)

#Save pins
@app.route('/save_pins/<img_id>')
def save_pins(img_id):
    if "username" not in session:
        return render_template("sign.html",display_nm="Author",error="You need to log in to save images.")
    
    #Save into db
    user_rec=users.query.filter_by(email=session["email"]).all()
    obj=saved_pins(user_id=user_rec[0].id,img_id=img_id)
    db.session.add(obj)
    db.session.commit ()

    return redirect(url_for('view_photo',photo_id=img_id))

@app.route('/view/<photo_id>', methods=["POST","GET"])
def view_photo(photo_id):
    if request.method=="POST":
        #Append dir path
        downloads = os.path.join(app.root_path, 'static/portal_images/')
        # Returning file from appended path
        return send_from_directory(directory=downloads, path=str(photo_id)+".jpg")

    if "username" not in session:
        nm="Author"
    else:
        nm=session["username"]
        if nm!="Admin":
            #Track visit 
            user_visited=users.query.filter_by(email=session["email"]).all()
            visit_obj = track_visits(user_id=user_visited[0].id, img_id=photo_id)
            db.session.add(visit_obj)
            db.session.commit()
    
    record_images=images.query.filter_by(id=photo_id).all()
    user_id=record_images[0].user_id
    user_details=users.query.filter_by(id=user_id).all()
    img_obj=images.query.filter_by(fields=record_images[0].fields).all()
    img_obj.pop(img_obj.index(record_images[0]))
    random.shuffle(img_obj)
    obj_follow=follow_user.query.filter_by(user_email=user_details[0].email).all()
    
    if "username" not in session:
        flag_follow=1
        flag_save=1

        return render_template("view-photo.html",display_nm=nm, img_data=record_images[0], user_data=user_details[0], 
    images_list=img_obj[:20], follow_count = len(obj_follow), flag_follow_check = flag_follow, flag_save_check=flag_save)

    obj_follow_check=follow_user.query.filter_by(user_email=user_details[0].email, follower_email=session["email"]).all()
    obj_users=users.query.filter_by(email=session["email"]).all()
    obj_save_check=saved_pins.query.filter_by(user_id=obj_users[0].id,img_id=photo_id).all()

    if session["email"]==user_details[0].email:
        flag_follow=0
    elif len(obj_follow_check)>0:
        flag_follow=0
    else:
        flag_follow=1

    if len(obj_save_check)>0:
        flag_save=0
    else:
        flag_save=1

    return render_template("view-photo.html",display_nm=nm, img_data=record_images[0], user_data=user_details[0], 
    images_list=img_obj[:20], follow_count = len(obj_follow), flag_follow_check = flag_follow, flag_save_check=flag_save)

@app.route('/author',methods=["GET","POST"])
def profile():
    nm=session["username"]

    if request.method=="GET":
        return render_template("profile.html",display_nm=nm)
    elif request.method=="":
        #Get input infos
        bio=request.form.get("bio")
        website=request.form.get("url")
        img=request.files["img"]
        read_img=Image.open(img)

        #Query 
        user_obj=users.query.filter_by(email=session["email"],name=session["username"]).all()
        user_id=user_obj[0].id

        read_img.save("static/portal_images/user"+str(user_id)+".jpg")

        links=website
        if 'www.' not in links:
            links='www.'+links
        if 'https' not in links or 'http' not in links:
            links='https://'+links

        #Create slug object
        obj=user_slugs(user_id=user_id,bio=bio,website=links)
        db.session.add(obj)
        db.session.commit()

        #Call function to generate updated ratings crosstab
        compute_user_similarity()

        return redirect(url_for('index'))


#Action means whether it's for login or for view of profile 
#Action 0 means to login and 1 means login to view profile

@app.route(r'/profile', defaults={'profile_email': "Default", "action":0})
@app.route(r'/profile/<profile_email>/<action>')
def profile_view(profile_email,action):
    if "username" not in session:
        nm="Author"
        if action==0:
            return render_template("sign.html",display_nm=nm)
        else:
            return render_template("sign.html",display_nm=nm,error="You need to log in to view profile of users.")
    elif session["username"]=="Admin":
        return redirect(url_for('index'))
    else:
        nm=session["username"]
        
        if profile_email=="Default":
            email=session["email"]
        else:
            email=profile_email
        obj=users.query.filter_by(email=email).all()
        user_id=obj[0].id
        slug_obj=user_slugs.query.filter_by(user_id=user_id).all()
        img_obj=images.query.filter_by(user_id=user_id).all()

        len_posts=len(img_obj)

        #Saved pins images 
        obj_users=users.query.filter_by(email=session["email"]).all()
        obj_saved_pins=saved_pins.query.filter_by(user_id=obj_users[0].id).all()

        for each in obj_saved_pins:
            img_id=each.id
            rec=images.query.filter_by(id=img_id).all()[0]
            if rec not in img_obj:
                img_obj.append(rec)

        obj_follow=follow_user.query.filter_by(user_email=profile_email).all()
        obj_following=follow_user.query.filter_by(follower_email=email).all()
        
        return render_template("profile_view.html",display_nm=nm,user_data=obj[0],slug_data=slug_obj[0],images_list=img_obj
        ,img_count=len_posts,follow_count=len(obj_follow),following_count=len(obj_following))


# Track analytics
def track_analytics(event_type, post_id=None):
    try:
        ip = request.remote_addr
        dt = datetime.now()
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        analytics_obj = analytics(event_type=event_type, post_id=post_id, ip_address=ip, timestamp=timestamp)
        db.session.add(analytics_obj)
        db.session.commit()
    except Exception as e:
        # Log error but don't crash the app
        print(f"Analytics tracking error: {e}")
        db.session.rollback()

# Blog posting route (for Ananya to post updates)
@app.route('/post',methods=["GET","POST"])
def post():
    # Check if logged in as Ananya
    if "username" not in session or session.get("username") != "Ananya Solanki":
        return redirect(url_for('login'))
    
    if request.method=="GET":
        categories = ["Work", "Life", "Projects", "Thoughts", "Updates"]
        return render_template("post.html", display_nm="Ananya Solanki", categories=categories)
    elif request.method=="POST":
        try:
            # Ensure database tables exist
            db.create_all()
            
            title = request.form.get("title")
            content = request.form.get("content")
            category = request.form.get("category")
            img = request.files.get("img")
            pdf = request.files.get("pdf")

            if not title or not content:
                categories = ["Work", "Life", "Projects", "Thoughts", "Updates"]
                return render_template("post.html", display_nm="Ananya Solanki", categories=categories, error="Title and content are required.")

            # Create date string
            dt = datetime.now()
            date_str = dt.strftime("%d %B, %Y")

            # Save blog post
            post_obj = blog_posts(
                title=title,
                content=content,
                category=category,
                created_at=date_str,
                show_date=True,  # Default to showing date
                author_id=1
            )
            db.session.add(post_obj)
            db.session.commit()

            post_id = post_obj.id
            print(f"✅ Post created with ID: {post_id}")

            # Save image if provided
            if img:
                try:
                    # Upload to Cloudinary
                    upload_result = cloudinary.uploader.upload(img)
                    image_path = upload_result['secure_url']
                    post_obj.image_path = image_path
                    db.session.commit()
                    print(f"✅ Image uploaded to Cloudinary: {image_path}")
                except Exception as e:
                    print(f"❌ Cloudinary upload failed: {e}")
                    # Fallback to local storage if Cloudinary fails (or dev mode without keys)
                    image = Image.open(img)
                    image_path = f"static/portal_images/blog_{post_id}.jpg"
                    image.save(image_path)
                    post_obj.image_path = image_path
                    db.session.commit()
            
            # Save PDF if provided
            if pdf and pdf.filename:
                try:
                    # Upload to Cloudinary
                    upload_result = cloudinary.uploader.upload(pdf, resource_type="raw")
                    pdf_path = upload_result['secure_url']
                    post_obj.pdf_path = pdf_path
                    db.session.commit()
                    print(f"✅ PDF uploaded to Cloudinary: {pdf_path}")
                except Exception as e:
                    print(f"❌ Cloudinary PDF upload failed: {e}")
                    # Fallback to local
                    pdf_dir = "static/portal_images/pdfs"
                    os.makedirs(pdf_dir, exist_ok=True)
                    
                    pdf_filename = f"blog_{post_id}_{pdf.filename}"
                    pdf_path = os.path.join(pdf_dir, pdf_filename)
                    pdf.save(pdf_path)
                    post_obj.pdf_path = pdf_path
                    db.session.commit()
            
            track_analytics("post_created", post_obj.id)
            categories = ["Work", "Life", "Projects", "Thoughts", "Updates"]
            return render_template("post.html", display_nm="Ananya Solanki", categories=categories, success="Glimpse published successfully! View it on the Glimpses page.")
        except Exception as e:
            print(f"❌ Error creating post: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            categories = ["Work", "Life", "Projects", "Thoughts", "Updates"]
            return render_template("post.html", display_nm="Ananya Solanki", categories=categories, error=f"Error saving post: {str(e)}")

# Delete post route
@app.route('/delete-post/<post_id>', methods=["POST"])
def delete_post(post_id):
    # Check if logged in as Ananya
    if "username" not in session or session.get("username") != "Ananya Solanki":
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        post = blog_posts.query.filter_by(id=post_id).first()
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Delete associated files if they exist locally
        if post.image_path and not post.image_path.startswith('http'):
            try:
                if os.path.exists(post.image_path):
                    os.remove(post.image_path)
            except Exception as e:
                print(f"⚠️ Could not delete image file: {e}")
        
        if post.pdf_path and not post.pdf_path.startswith('http'):
            try:
                if os.path.exists(post.pdf_path):
                    os.remove(post.pdf_path)
            except Exception as e:
                print(f"⚠️ Could not delete PDF file: {e}")
        
        # Delete from database
        db.session.delete(post)
        db.session.commit()
        
        print(f"✅ Post {post_id} deleted successfully")
        return jsonify({"success": True, "message": "Post deleted successfully"})
    except Exception as e:
        print(f"❌ Error deleting post: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Toggle date visibility route
@app.route('/toggle-date/<post_id>', methods=["POST"])
def toggle_date(post_id):
    # Check if logged in as Ananya
    if "username" not in session or session.get("username") != "Ananya Solanki":
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        post = blog_posts.query.filter_by(id=post_id).first()
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Toggle show_date
        post.show_date = not post.show_date
        db.session.commit()
        
        print(f"✅ Date visibility toggled for post {post_id}: {post.show_date}")
        return jsonify({"success": True, "show_date": post.show_date})
    except Exception as e:
        print(f"❌ Error toggling date: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Edit post route
@app.route('/edit-post/<post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    # Check if logged in as Ananya
    if "username" not in session or session.get("username") != "Ananya Solanki":
        return redirect(url_for('login'))
    
    post = blog_posts.query.filter_by(id=post_id).first()
    if not post:
        return redirect(url_for('glimpses'))
    
    if request.method == "GET":
        categories = ["Work", "Life", "Projects", "Thoughts", "Updates"]
        return render_template("edit_post.html", display_nm="Ananya Solanki", post=post, categories=categories)
    
    elif request.method == "POST":
        try:
            # Update post fields
            post.title = request.form.get("title", post.title)
            post.content = request.form.get("content", post.content)
            post.category = request.form.get("category", post.category)
            
            # Update show_date toggle
            show_date = request.form.get("show_date")
            post.show_date = (show_date == "on" or show_date == "true")
            
            # Handle image update
            img = request.files.get("img")
            if img and img.filename:
                try:
                    # Try Cloudinary first
                    upload_result = cloudinary.uploader.upload(img)
                    image_path = upload_result['secure_url']
                    post.image_path = image_path
                    print(f"✅ Image updated on Cloudinary: {image_path}")
                except Exception as e:
                    print(f"❌ Cloudinary upload failed: {e}")
                    # Fallback to local storage
                    image = Image.open(img)
                    image_path = f"static/portal_images/blog_{post_id}.jpg"
                    image.save(image_path)
                    post.image_path = image_path
                    db.session.commit()
            
            # Handle PDF update
            pdf = request.files.get("pdf")
            if pdf and pdf.filename:
                try:
                    # Try Cloudinary first
                    upload_result = cloudinary.uploader.upload(pdf, resource_type="raw")
                    pdf_path = upload_result['secure_url']
                    post.pdf_path = pdf_path
                    print(f"✅ PDF updated on Cloudinary: {pdf_path}")
                except Exception as e:
                    print(f"❌ Cloudinary PDF upload failed: {e}")
                    # Fallback to local storage
                    pdf_dir = "static/portal_images/pdfs"
                    os.makedirs(pdf_dir, exist_ok=True)
                    pdf_filename = f"blog_{post_id}_{pdf.filename}"
                    pdf_path = os.path.join(pdf_dir, pdf_filename)
                    pdf.save(pdf_path)
                    post.pdf_path = pdf_path
            
            # Save changes
            db.session.commit()
            print(f"✅ Post {post_id} updated successfully")
            
            return redirect(url_for('glimpse_post', post_id=post_id))
        except Exception as e:
            print(f"❌ Error updating post: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            categories = ["Work", "Life", "Projects", "Thoughts", "Updates"]
            return render_template("edit_post.html", display_nm="Ananya Solanki", post=post, categories=categories, error=f"Error updating post: {str(e)}")

@app.route('/logout')
def logout():
    session.pop("username")
    session.pop("email")
    return redirect(url_for("index"))

@app.route('/register', methods=["GET","POST"])
def register():
    if "username" in session:
        nm=session["username"]
    else:
        nm="Author"

    if request.method == "GET":
        cat_records=pin_category.query.all()
        return render_template("signup.html",display_nm=nm,categories=cat_records)
    elif request.method == "POST":
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        full_name=fname+" "+lname
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        interest_list=request.form.getlist("int")

        new_string=""
        for ls in interest_list:
            new_string=new_string+ls+","
        
        user_obj = users(name=full_name, email=email, password=pwd, interests=new_string[:-1])
        db.session.add(user_obj)
        db.session.commit()
            
        #Set session object 
        session["username"]=full_name
        session["email"]=email
        return redirect(url_for("profile"))
    else:
        return "404, Access not Allowed!"

# Subscribe route
@app.route('/subscribe', methods=["POST"])
def subscribe():
    email = request.form.get("email")
    name = request.form.get("name", "")
    
    if email:
        # Check if already subscribed
        existing = subscribers.query.filter_by(email=email).first()
        if existing:
            track_analytics("subscribe", None)
            return redirect(url_for('index') + '?subscribed=already')
        
        dt = datetime.now()
        date_str = dt.strftime("%d %B, %Y")
        
        subscriber = subscribers(email=email, name=name, subscribed_at=date_str, is_active=True)
        db.session.add(subscriber)
        db.session.commit()
        track_analytics("subscribe", None)
        return redirect(url_for('index') + '?subscribed=success')
    
    return redirect(url_for('index'))

@app.route('/analytics-data')
def analytics_data():
    if "username" not in session or session.get("username") != "Ananya Solanki":
        return jsonify({"error": "Unauthorized"}), 403
    
    total_views = analytics.query.filter_by(event_type="view").count()
    total_shares = analytics.query.filter_by(event_type="share").count()
    total_downloads = analytics.query.filter_by(event_type="download").count()
    total_pdfs = analytics.query.filter_by(event_type="pdf_download").count()
    total_subscribers = subscribers.query.filter_by(is_active=True).count()
    total_posts = blog_posts.query.count()
    
    return jsonify({
        "views": total_views,
        "shares": total_shares,
        "downloads": total_downloads,
        "pdfs": total_pdfs,
        "subscribers": total_subscribers,
        "posts": total_posts
    })

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html", display_nm="Ananya Solanki")

@app.route('/api/chat', methods=["POST"])
def chat_api():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get API key from config, environment variable, or default
        api_key = CONFIG_API_KEY or os.environ.get("ANTHROPIC_API_KEY") or "sk-ant-api03-Your-Key-Here"
        
        # Check if using placeholder key
        if api_key == "sk-ant-api03-Your-Key-Here":
            return jsonify({"error": "Please set your Anthropic API key in config.py or as ANTHROPIC_API_KEY environment variable"}), 500
        
        # System prompt with Ananya's personality and full career/work experience
        system_prompt = """You are Ms. Matterhorn, Ananya Solanki's AI counterpart. You are a professional, warm, and authentic Indian American business analyst and consultant.

YOUR PERSONALITY:
- Professional yet approachable - maintain a balanced, mature tone like a thoughtful colleague
- Warm and genuine - connect authentically without being overly enthusiastic
- Supportive and encouraging - help others while staying grounded
- Intelligent and analytical - think through problems carefully and provide data-driven insights
- Culturally aware - naturally blend Indian and American perspectives

YOUR BACKGROUND:
- Born in Janakpuri, Delhi, India; grew up in Delhi
- Moved to USA for Masters in Applied Business Analytics at Boston University
- Currently working in the USA and looking for new opportunities

YOUR COMPLETE CAREER & WORK EXPERIENCE:

1. BUSINESS DEVELOPMENT ANALYST | IDORI | Boston, MA | March 2024 – Present
   - Leverage SQL to query marketing, product, and metadata sources; perform exploratory analysis to surface ICP patterns, emerging category whitespace, and SKU-level trends
   - Build Tableau + HubSpot BI dashboards to visualize pipeline health, campaign engagement, and segment performance
   - Design lightweight data workflows and CRM data models to improve lead scoring, segmentation, and data hygiene across HubSpot and Apollo
   - Partner with Product, Marketing, and Operations to translate insights into channel messaging and collateral refinements
   - Lead consultative discovery and close recurring partnerships with SMB brands
   - Key achievements: 40% reduction in manual reporting time, 25% increase in conversion velocity, 35% improvement in outbound response rates

2. PRODUCT ANALYST | Ogrelogic | Austin, TX | August 2021 – August 2023
   - Led business case modeling for new service lines and pricing structures
   - Automated SQL-based performance dashboards tracking CAC, LTV, and retention across digital products
   - Delivered executive insight reports highlighting revenue levers, scenario models, and recommended actions
   - Partnered with Marketing, Engineering, and Ops to translate data findings into channel + product optimization initiatives
   - Conducted experimentation and behavioral analysis to identify key conversion drivers
   - Key achievements: 18% improvement in gross margins, 50% reduction in analysis turnaround time, 20%+ increase in feature adoption, 15% uplift in user activation

3. STRATEGY CONSULTANT | Boston University Consulting Group | Boston, MA | September 2023 – December 2024
   - Led a 5-person team in consulting a merchandising client on customer retention and operational efficiency initiatives
   - Conducted quantitative research and market segmentation analysis to identify high-value customer cohorts and growth opportunities
   - Created KPI scorecards, business memos, and strategy decks for client presentations

KEY PROJECTS:
- Market Expansion Strategy: Sized new U.S. healthcare distribution market for CPG client, evaluated market entry risks, modeled 3-year revenue potential
- Retention Analytics Dashboard: Built cohort retention model integrating customer, churn, and marketing spend data to inform campaign optimization
- Dyson Dissection - MyDyson App Redesign: Led UX redesign as Product Manager, directed UX research with 15+ user interviews, redesigned Setup/Support/Maintenance flows

TECHNICAL SKILLS:
- Analytics & Modeling: Excel (Advanced), SQL, Python, Power BI, Tableau
- Strategy & Planning: Business Case Development, Market Sizing, KPI Design, Forecast Modeling, Competitive Analysis
- Data Infrastructure: ETL Pipelines, API Integration, Data Cleaning, Automation (n8n, VBA)
- Visualization & Communication: Dashboarding, Data Storytelling, Executive Presentations, Memos
- Tools: Asana, Jira, Confluence, Figma, Google Workspace, HubSpot, Apollo

CERTIFICATIONS:
- Inside LVMH Certificate - Creation and Branding, Operations and Supply Chain in Luxury Markets
- Lean Six Sigma Green Belt
- Microsoft Power BI Analyst
- Certified Scrum Product Owner (CSPO)

COMMUNICATION GUIDELINES:
- Respond like a proper AI chatbot: clear, structured, helpful, and professional
- Use Ananya's character traits naturally: warm, authentic, culturally aware, but not overly animated
- Use "yaar" occasionally when it feels authentic, not forced
- Avoid: excessive excitement markers, "*jumps*", "*squeals*", or overly animated phrases
- When discussing data, calculations, or analysis: provide clear, structured responses with numbers separated
- For intellectual questions: break down complex topics into digestible insights
- Reference your actual work experience and projects when relevant

RESPONSE FORMAT FOR CALCULATIONS/INTELLECTUAL CONTENT:
When the question involves calculations, data analysis, or intellectual reasoning:
1. Provide a brief explanation
2. Present key numbers/calculations in a clear, structured format (use bullet points or numbered lists)
3. Add context and insights

Format numbers clearly:
• Revenue: $X
• Growth rate: Y%
• Projected: $Z
• Conversion: A%

Remember: You're Ananya's professional AI counterpart. Be genuine, helpful, and maintain a natural, professional tone that reflects her expertise, work experience, and warmth without being overly animated. You know her entire career history and can reference specific projects, achievements, and skills when relevant."""
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Use claude-3-haiku-20240307 which is confirmed to work with this API key
        # This is a fast and capable model suitable for chatbot interactions
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ],
            timeout=60.0
        )
        
        response_text = message.content[0].text
        
        # Detect if response contains calculations or numbers
        import re
        has_calculations = False
        calculation_data = None
        
        # Check for calculation patterns (numbers, percentages, formulas, etc.)
        calc_patterns = [
            r'\$\d+[,\d]*',  # Money amounts
            r'\d+%',  # Percentages
            r'\d+\.\d+%',  # Decimal percentages
            r'=\s*\d+',  # Equals calculations
            r'\d+\s*[+\-*/]\s*\d+',  # Math operations
            r'Revenue|Growth|ROI|CAC|LTV|Conversion|Analysis|Metric|KPI',  # Business metrics
        ]
        
        has_numbers = bool(re.search(r'\d+', response_text))
        has_calc_keywords = any(re.search(pattern, response_text, re.IGNORECASE) for pattern in calc_patterns)
        user_asked_calc = any(word in user_message.lower() for word in ['calculate', 'calculation', 'compute', 'analysis', 'data', 'number', 'metric', 'kpi', 'revenue', 'growth'])
        
        if has_numbers and (has_calc_keywords or user_asked_calc):
            has_calculations = True
            # Extract numbers from response
            numbers = re.findall(r'\$?\d+[,\d]*(?:\.\d+)?%?', response_text)
            # Also extract bullet points with numbers
            bullet_numbers = re.findall(r'[•\-\*]\s*[^:]*:\s*\$?\d+[,\d]*(?:\.\d+)?%?', response_text)
            
            all_numbers = list(set(numbers[:15]))  # Limit to 15 unique numbers
            if bullet_numbers:
                all_numbers.extend([re.findall(r'\$?\d+[,\d]*(?:\.\d+)?%?', b)[0] for b in bullet_numbers[:5] if re.findall(r'\$?\d+[,\d]*(?:\.\d+)?%?', b)])
            
            if all_numbers:
                calculation_data = {
                    "numbers": list(set(all_numbers))[:10]  # Limit to 10 unique numbers
                }
        
        return jsonify({
            "response": response_text,
            "has_calculations": has_calculations,
            "calculation_data": calculation_data
        })
        
    except anthropic.APIError as e:
        print(f"Anthropic API Error: {e}")
        return jsonify({"error": f"API Error: {str(e)}"}), 500
    except Exception as e:
        print(f"Chat API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/login', methods=["GET","POST"])
def login():
    if "username" in session:
        return redirect(url_for("post"))

    if request.method == "GET":
        return render_template("signin.html", display_nm="Ananya Solanki")
    elif request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")

        # Ananya's login
        if email == "anamatterhorn" and pwd == "manifesting_majestic_moments":
            session["email"] = "ananyasolanki9099@gmail.com"
            session["username"] = "Ananya Solanki"
            track_analytics("login", None)
            return redirect(url_for("post"))
        else:
            return render_template("signin.html", display_nm="Ananya Solanki", error="Wrong email or Password entered!")
    else:
        return "404, Access not Allowed!"


if __name__=="__main__":
    # Get port from environment variable (for deployment) or default to 8000
    port = int(os.environ.get('PORT', 8000))
    # Only run in debug mode if not in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)