# 🍶 Flask Projects - Web Framework Fundamentals

A **comprehensive Flask portfolio** demonstrating modern web development patterns including authentication, database ORM, RESTful APIs, form handling, and deployment strategies for production-grade applications.

## 🎯 Overview

This project showcases:
- ✅ Flask application structure & blueprints
- ✅ SQLAlchemy ORM & database design
- ✅ User authentication & authorization
- ✅ RESTful API design
- ✅ Form validation & CSRF protection
- ✅ Jinja2 templating
- ✅ Error handling & logging
- ✅ Deployment & configuration management

## 🏗️ Architecture

### Flask Application Structure
```
flask_app/
├── app.py                 # Application factory
├── config.py             # Configuration management
├── requirements.txt      # Dependencies
├── wsgi.py              # WSGI entry point
├── app/
│   ├── __init__.py
│   ├── models/          # Database models
│   │   ├── user.py
│   │   └── post.py
│   ├── routes/          # Blueprints
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── api.py
│   ├── templates/       # Jinja2 templates
│   │   ├── base.html
│   │   ├── home.html
│   │   └── auth/
│   └── static/          # Assets
│       ├── css/
│       └── js/
└── tests/               # Unit tests
    └── test_routes.py
```

### Tech Stack
| Component | Technology |
|-----------|-----------|
| **Framework** | Flask 2.x |
| **Database** | SQLAlchemy ORM, SQLite/PostgreSQL |
| **Forms** | Flask-WTF, WTForms |
| **Auth** | Flask-Login, bcrypt |
| **API** | Flask-RESTful, Flask-CORS |
| **Task Queue** | Celery (optional) |
| **Deployment** | Gunicorn, Nginx |

## 🔧 Core Components

### Application Factory Pattern

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from app.routes import auth_bp, main_bp, api_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
```

### Configuration Management

```python
# config.py
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Session configuration
    SESSION_COOKIE_SECURE = True      # HTTPS only
    SESSION_COOKIE_HTTPONLY = True    # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True  # Log SQL queries

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # Use PostgreSQL in production
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_PRE_PING = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

## 🗄️ Database & Models

### SQLAlchemy ORM

```python
# app/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    """User model with authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                           cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash password using bcrypt"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Serialize to JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# app/models/post.py
class Post(db.Model):
    """Blog post model"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
                       nullable=False, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.isoformat()
        }
```

## 🔐 Authentication & Authorization

### User Registration & Login

```python
# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_has_safe_scheme
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with validation"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with session management"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Verify credentials
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # Redirect to next page or index
            next_page = request.args.get('next')
            if next_page and url_has_safe_scheme(next_page):
                return redirect(next_page)
            return redirect(url_for('main.index'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
```

### Form Validation with CSRF

```python
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    """Registration form with validation"""
    username = StringField('Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]
    )
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Custom validator for duplicate username"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    """Blog post form"""
    title = StringField('Title',
        validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content',
        validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Post')
```

## 🔌 RESTful API Design

### Flask-RESTful Endpoints

```python
# app/routes/api.py
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_cors import cross_origin
from app.models import User, Post
from app import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class UserListAPI(Resource):
    """Handle multiple users"""
    
    def get(self):
        """Get all users with pagination"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        paginated = User.query.paginate(page=page, per_page=per_page)
        
        return {
            'users': [u.to_dict() for u in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }, 200
    
    def post(self):
        """Create new user (admin only)"""
        if not current_user or not current_user.is_admin:
            return {'error': 'Unauthorized'}, 403
        
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        
        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict(), 201

class UserDetailAPI(Resource):
    """Handle single user"""
    
    def get(self, user_id):
        """Get specific user"""
        user = User.query.get_or_404(user_id)
        return user.to_dict(), 200
    
    def put(self, user_id):
        """Update user"""
        user = User.query.get_or_404(user_id)
        if user != current_user:
            return {'error': 'Unauthorized'}, 403
        
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        
        if args['email']:
            user.email = args['email']
        if args['username']:
            user.username = args['username']
        
        db.session.commit()
        return user.to_dict(), 200
    
    def delete(self, user_id):
        """Delete user"""
        user = User.query.get_or_404(user_id)
        if user != current_user:
            return {'error': 'Unauthorized'}, 403
        
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200

# Register API endpoints
api.add_resource(UserListAPI, '/users')
api.add_resource(UserDetailAPI, '/users/<int:user_id>')
```

## 🌐 Templating with Jinja2

### Base Template & Inheritance

```html
<!-- app/templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <a href="{{ url_for('main.index') }}">Home</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('main.dashboard') }}">Dashboard</a>
            <a href="{{ url_for('auth.logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('auth.login') }}">Login</a>
            <a href="{{ url_for('auth.register') }}">Register</a>
        {% endif %}
    </nav>
    
    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <!-- Main content -->
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>

<!-- app/templates/auth/login.html -->
{% extends "base.html" %}
{% block title %}Login{% endblock %}
{% block content %}
    <div class="login-container">
        <h1>Login</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.email.label }}
                {{ form.email(class="form-control") }}
                {% if form.email.errors %}
                    <span class="error">{{ form.email.errors[0] }}</span>
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.password.label }}
                {{ form.password(class="form-control", type="password") }}
            </div>
            <div class="form-group">
                {{ form.remember_me() }} {{ form.remember_me.label }}
            </div>
            {{ form.submit(class="btn btn-primary") }}
        </form>
    </div>
{% endblock %}
```

## 🚀 Deployment

### Gunicorn & Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file for secrets
echo "SECRET_KEY=$(python -c 'import os; print(os.urandom(32).hex())')" > .env
echo "DATABASE_URL=postgresql://user:pass@localhost/flaskapp" >> .env

# Export Flask app
export FLASK_APP=wsgi.py
export FLASK_ENV=production

# Run with Gunicorn (production)
gunicorn --worker-class sync --workers 4 --threads 2 \
         --worker-connections 1000 --max-requests 1000 \
         --timeout 30 --bind 0.0.0.0:5000 wsgi:app
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/flaskapp
upstream flaskapp {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    server_name example.com;
    
    client_max_body_size 5M;
    
    location / {
        proxy_pass http://flaskapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 💡 Interview Questions

### Q: How is Flask different from Django?
```
Flask:
- Micro-framework (minimal dependencies)
- Flexible, build-your-own stack
- Good for APIs and custom solutions
- Easier learning curve

Django:
- Full-featured framework
- Batteries included (ORM, auth, admin)
- Faster development for large apps
- Opinionated structure

**Choose Flask when**: Building APIs, microservices, custom requirements
**Choose Django when**: Need rapid development, batteries-included features
```

### Q: How do you handle database migrations?
```
Use Flask-Migrate (wrapper around Alembic):

# Create migration
flask db init
flask db migrate -m "Add user table"
flask db upgrade

# Each migration creates version control for DB schema
# Easy rollback: flask db downgrade
```

## 🌟 Portfolio Value

✅ Complete web application architecture
✅ Professional authentication patterns
✅ RESTful API design
✅ Database design & ORM expertise
✅ Security best practices (CSRF, password hashing)
✅ Production deployment ready
✅ Scalable blueprint structure

## 📄 License

MIT License - Educational Use

---

**Next Development**:
1. Add Celery for async tasks
2. Implement caching layer
3. Add comprehensive logging
4. CI/CD pipeline setup
5. WebSocket real-time updates
