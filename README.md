# 🌐 Flask Projects - Web Backend Development

A **collection of Flask web applications** demonstrating REST API development, database integration, authentication, and deployment for production-ready web services.

## 🎯 Overview

This project covers:
- ✅ Flask fundamentals & routing
- ✅ RESTful API design
- ✅ Database integration (SQLAlchemy)
- ✅ User authentication & authorization
- ✅ Form handling & validation
- ✅ Error handling & logging
- ✅ Deployment strategies

## 🏗️ Flask Application Architecture

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import logging

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Extensions
db = SQLAlchemy(app)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppConfig:
    """Application configuration"""
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'jwt-secret'
```

## 📦 Database Models

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """Hash password"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verify password"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    """Post model"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author.username,
            'created_at': self.created_at.isoformat()
        }
```

## 🔌 RESTful API Routes

```python
from flask import Flask, request, jsonify
from functools import wraps
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

# JWT setup
jwt = JWTManager(app)

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    # Validation
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    # Create user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created', 'user': user.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT
    access_token = create_access_token(identity=user.id)
    
    return jsonify({'access_token': access_token}), 200

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages
    }), 200

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create post (requires auth)"""
    from flask_jwt_extended import get_jwt_identity
    
    data = request.get_json()
    user_id = get_jwt_identity()
    
    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=user_id
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({'message': 'Post created', 'post': post.to_dict()}), 201

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get single post"""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update post"""
    from flask_jwt_extended import get_jwt_identity
    
    post = Post.query.get_or_404(post_id)
    user_id = get_jwt_identity()
    
    # Check ownership
    if post.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    
    db.session.commit()
    
    return jsonify({'message': 'Post updated', 'post': post.to_dict()}), 200
```

## 🔐 Authentication & Authorization

```python
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    """Check if user logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard"""
    return jsonify({'message': f'Welcome {session["username"]}'}), 200
```

## 🧪 Testing

```python
import unittest
from flask_testing import FlaskTestCase

class TestAPI(FlaskTestCase):
    """API tests"""
    
    def create_app(self):
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_register(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', response.json)
    
    def test_get_posts(self):
        """Test get posts"""
        response = self.client.get('/api/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.json)
```

## 🚀 Deployment

```python
# Gunicorn configuration
app_workers = 4
app_thread_per_worker = 2
app_timeout = 120

# Docker deployment
docker_config = """
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
"""

# Environment variables
env_config = {
    'FLASK_ENV': 'production',
    'DATABASE_URL': 'postgresql://user:pass@localhost/dbname',
    'SECRET_KEY': 'production-secret-key',
    'JWT_SECRET_KEY': 'jwt-secret-key'
}
```

## 💡 Interview Talking Points

**Q: Design REST API?**
```
Answer:
- Resource-based endpoints
- HTTP verbs (GET/POST/PUT/DELETE)
- Status codes (200/201/400/401/404)
- Error handling
- Pagination & filtering
- API versioning
```

**Q: Security best practices?**
```
Answer:
- JWT tokens for auth
- Password hashing (bcrypt)
- CORS configuration
- Input validation
- Rate limiting
- HTTPS enforcement
```

## 🌟 Portfolio Value

✅ Flask fundamentals
✅ RESTful API design
✅ Database ORM (SQLAlchemy)
✅ Authentication (JWT)
✅ Error handling
✅ Testing strategies
✅ Deployment ready

---

**Technologies**: Flask, SQLAlchemy, JWT, Gunicorn, Docker

