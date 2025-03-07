import os
import json
import re
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import db, Contacts, Posts, User
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration
with open('config.json','r') as c:
    params = json.load(c)["params"]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Flask app setup
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', params.get('secret_key', 'default-secret-key'))

# Upload folder setup
UPLOAD_FOLDER = "static/assets/img"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Configuration
local_server = os.getenv('LOCAL_SERVER', 'True').lower() == 'true'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('LOCAL_URL') if local_server else os.getenv('PROD_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# Helper function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Ensure database tables are created
with app.app_context():
    db.create_all()

# Blog Configurations
blog_name = os.getenv('BLOG_NAME', 'Default Blog')
about_txt = os.getenv('ABOUT_TXT', 'About me section')
no_of_posts = int(os.getenv('NO_OF_POSTS', '2'))

# Routes
@app.route("/")
def home():
    page = max(1, request.args.get('page', 1, type=int))
    per_page = int(params.get('no_of_posts', 2))
    posts = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    prev_url = url_for("home", page=posts.prev_num) if posts.has_prev else None
    next_url = url_for("home", page=posts.next_num) if posts.has_next else None

    return render_template('index.html', params=params, posts=posts.items, prev=prev_url, next=next_url)

@app.route("/about",methods=['GET'])
def about():
        return (render_template('about.html',params = params))

@app.route("/post", methods=['GET', 'POST'])
def post():
    if 'user' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    user_email = session.get('user')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        session.pop('user', None)
        flash("User not found!", "danger")
        return redirect(url_for("login"))

    # Pagination Setup
    page = max(1, request.args.get('page', 1, type=int))
    per_page = 3
    user_posts = Posts.query.filter_by(user_id=user.id).order_by(Posts.date.desc()).paginate(page=page,per_page=per_page,error_out=False)
    prev_url = url_for("post", page=user_posts.prev_num) if user_posts.has_prev else None
    next_url = url_for("post", page=user_posts.next_num) if user_posts.has_next else None
    return render_template('post.html', posts=user_posts.items, user=user, prev=prev_url, next=next_url,params=params)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if 'user' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    user_email = session.get('user')
    user = User.query.filter_by(email=user_email).first()

    if not user:
        session.pop('user', None)
        flash("User not found!", "danger")
        return redirect(url_for("login"))

    page = max(1, request.args.get('page', 1, type=int))
    per_page = 3
    user_posts = Posts.query.filter_by(user_id=user.id).order_by(Posts.date.desc()).paginate(page=page,per_page=per_page,error_out=False)

    return render_template('dashboard.html', params=params, posts=user_posts)

@app.route("/add",methods=['POST'])
def add_post():
    if 'user' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    user = User.query.filter_by(email=session.get('user')).first()

    if not user:
        flash("Invalid user session! Please log in again.", "danger")
        session.pop('user', None)
        return redirect(url_for("login"))

    if request.method == 'POST':
        title = request.form['title']
        slug = request.form['slug']
        content = request.form['content']
        date = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        img_file = request.files.get('img_file')

        if not (title and slug and content):
            flash("All fields are required!", 'danger')
            return render_template("add.html", params=params)

        existing_slug = Posts.query.filter_by(slug=slug).first()
        if existing_slug:
            flash("Slug already exists! Please choose a different one.", "danger")
            return render_template("add.html", params=params)

        filename = secure_filename(img_file.filename) if img_file and img_file.filename else None
        if filename:
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = Posts(title=title, slug=slug, content=content, date=date, img_file=filename , user_id=user.id)
        db.session.add(new_post)
        db.session.commit()
        flash("New post added!", "success")
        return redirect(url_for("dashboard"))
    return render_template("add.html", params=params)

@app.route("/edit/<int:sno>", methods=['GET', 'PUT'])
def edit_post(sno):
    if 'user' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash("Invalid session! Please log in again.", "danger")
        session.clear()
        return redirect(url_for("login"))

    post = Posts.query.get_or_404(sno)
    if not post:
        flash("Post not found!", "danger")
        return redirect(url_for("dashboard"))

    if post.user_id != user.id:
        flash("You are not authorized to edit this post!", "danger")
        return redirect(url_for("dashboard"))

    if request.method == 'POST':
        title = request.form['title']
        slug = request.form['slug']
        content = request.form['content']
        post.date = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        img_file = request.files.get('img_file')

        existing_slug = Posts.query.filter(Posts.slug == slug, Posts.sno != sno).first()
        if existing_slug:
            flash("Slug already exists! Please choose a different one.", "danger")
            return redirect(url_for("edit_post", sno=sno))
        post.title = title
        post.slug = slug
        post.content = content

        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            post.img_file = filename

        db.session.commit()
        flash("Post Updated Successfully", "success")
        return redirect(url_for("dashboard"))
    return render_template("edit.html", post=post, params=params, sno=sno)

@app.route("/post/<string:post_slug>",methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    if post:
        return render_template('post_slug.html', params=params, post=post)
    else:
        flash("Post not found!", "danger")
        return redirect(url_for("home"))

@app.route("/delete/<int:sno>", methods=['DELETE'])
def delete(sno):
    if 'user' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    user = User.query.filter_by(email=session['user']).first()
    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("login"))

    post = Posts.query.filter_by(sno=sno).first()
    if not post:
        flash("Post not found!", "warning")
        return redirect(url_for("dashboard"))

    if post.user_id != user.id:  # Ensure only author can delete
        flash("You are not authorized to delete this post!", "danger")
        return redirect(url_for("dashboard"))

    try:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting post: {str(e)}", "danger")

    return redirect(url_for("dashboard"))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()
        date = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        # Regular expressions for validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^\d{10}$'

        if not name or not email or not message:
            flash("Name, email, and message are required fields!", "danger")
            return redirect(url_for("contact"))

        if not re.match(email_regex, email):
            flash("Invalid email format!", "danger")
            return redirect(url_for("contact"))

        if phone and not re.match(phone_regex, phone):
            flash("Invalid phone number! Must be 10 digits.", "danger")
            return redirect(url_for("contact"))

        try:
            new_contact = Contacts(name=name, email=email, ph_no=phone, msg=message, date=date)
            db.session.add(new_contact)
            db.session.commit()

            # Send email to admin
            admin_email = app.config['MAIL_USERNAME']
            subject = f"New Contact Form Submission from {name}"
            body = f"""
            Name: {name}
            Email: {email}
            Phone: {phone if phone else 'Not provided'}
            Message: {message}
            Date: {date}
            """

            msg = Message(subject, sender=email, recipients=[admin_email])
            msg.body = body
            mail.send(msg)

            flash("Your message has been sent successfully!", "success")
            return redirect(url_for("contact"))

        except Exception as e:
            db.session.rollback()
            flash("Something went wrong! Please try again later.", "danger")
            app.logger.error(f"Contact form submission error: {str(e)}")

    return render_template('contact.html', params=params)

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' not in session:
        flash("You are not logged in.", "warning")
        return redirect(url_for("home"))

    session.pop('user', None)
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'user' in session:
        return redirect(url_for("dashboard"))

    if request.method == 'POST':
        name, email, password = request.form['name'], request.form['email'], request.form['password']

        # Name validation: Only letters and spaces allowed
        if not re.match(r"^[A-Za-z\s]+$", name):
            flash("Name must contain only letters and spaces.", "danger")
            return redirect(url_for("register"))

        # Email validation: Must be in a valid email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "danger")
            return redirect(url_for("register"))

        # Password validation: At least 8 characters, 1 number, 1 uppercase letter
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
            flash("Password must be at least 8 characters long and include at least one number and one uppercase letter.", "danger")
            return redirect(url_for("register"))

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))

        # Save user to the database with hashed password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully!', 'success')
        return redirect(url_for("login"))

    return render_template('register.html',params=params)

@app.route('/login',methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for("dashboard"))
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = user.email
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid email or password!", "danger")
    return render_template('login.html', params=params)

@app.route("/search",methods = ['GET','POST'])
def search():
    posts = Posts.query.all()
    if request.method == 'POST':
        query = request.form.get('search')

        if not query.strip():
            flash("Please enter a search term!", "warning")
            return redirect(url_for("dashboard"))

        results = Posts.query.filter(Posts.title.ilike(f"%{query}%")).all()
        return render_template('dashboard.html', results=results, query=query, params=params, posts=posts)

    return render_template('dashboard.html',params=params,posts=posts)

if __name__ == "__main__":
    app.run(debug=True)

