# Flask Projects

A comprehensive collection of Flask web application projects demonstrating various functionalities and best practices in Python web development.

## Overview

This repository contains multiple Flask-based web applications showcasing different aspects of modern web development including user authentication, file uploads, database integration, and real-time search capabilities.

## Projects Included

### 1. **Main Application (app.py)**
Core Flask application with:
- Database integration
- User management
- RESTful API endpoints
- Template rendering with Jinja2
- Static file serving

### 2. **Search Module (search.py)**
Advanced search functionality:
- Full-text search capabilities
- Filter and sorting options
- Query optimization
- Results pagination
- Search analytics

### 3. **Safety Module (safety.py)**
Security and validation features:
- Input validation and sanitization
- CSRF protection
- SQL injection prevention
- Password hashing and verification
- Rate limiting

## Features

- **User Authentication**: Secure login/registration system
- **File Upload**: Handle file uploads with validation
- **Database Operations**: SQLAlchemy ORM integration
- **Search Functionality**: Efficient querying and filtering
- **API Endpoints**: RESTful API design
- **Error Handling**: Comprehensive error management
- **Logging**: Application logging and debugging

## Technology Stack

- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM (relational databases)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login / Session management
- **Validation**: WTForms for form validation
- **Security**: CSRF tokens, password hashing

## Project Structure

```
flask_projects/
├── app.py                 # Main Flask application
├── search.py              # Search functionality module
├── safety.py              # Security utilities module
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── dashboard.html
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── instance/              # Instance folder (config, data)
├── uploads/               # User uploaded files
└── django/                # Django-related files (if integrated)
```

## Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Virtual environment (recommended)

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/Sunny-commit/flask_projects.git
cd flask_projects
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install flask flask-sqlalchemy flask-login wtforms
```

4. Configure environment variables
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

5. Initialize database
```bash
python
>>> from app import db
>>> db.create_all()
```

6. Run the application
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Usage

### User Authentication
- Register a new account on the registration page
- Login with your credentials
- Access protected routes after authentication

### File Upload
- Navigate to upload section
- Select file from your system
- File validation occurs server-side
- Uploaded files stored in `/uploads` directory

### Search Functionality
- Use search bar to query database
- Apply filters for refined results
- Sort by relevance, date, or custom fields
- View paginated results

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| POST | `/register` | User registration |
| POST | `/login` | User login |
| GET | `/logout` | User logout |
| POST | `/search` | Search functionality |
| POST | `/upload` | File upload |
| GET | `/dashboard` | User dashboard |

## Configuration

### Database Configuration
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Security Settings
```python
SECRET_KEY = 'your-secret-key-here'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

## Security Features

- **CSRF Protection**: Enabled on all forms
- **Password Security**: Salted password hashing
- **SQL Injection Prevention**: Parametrized queries
- **XSS Protection**: Template auto-escaping
- **Rate Limiting**: Request throttling

## Error Handling

- Custom error pages (404, 500, etc.)
- Detailed logging for debugging
- User-friendly error messages
- Exception handling middleware

## Testing

Run tests with pytest:
```bash
pip install pytest
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Best Practices Used

- Modular code structure
- Separation of concerns
- Security-first approach
- Error handling and logging
- DRY principles
- Configuration management
- Database abstraction with ORM

## Common Issues & Troubleshooting

### Port Already in Use
```bash
flask run --port 5001
```

### Database Errors
```bash
# Reset database
rm instance/app.db
python -c "from app import db; db.create_all()"
```

### Module Not Found
```bash
pip install -r requirements.txt
```

## Performance Optimization

- Database query optimization
- Caching mechanisms
- Asset minification
- Connection pooling
- Lazy loading implementation

## Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Configure HTTPS/SSL
- [ ] Set up database backups
- [ ] Enable monitoring and logging
- [ ] Configure CDN for static files

### Production Server Example
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Author

Pateti Chandu (Sunny-commit)

## License

MIT License - feel free to use this project for educational and commercial purposes.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Roadmap

- [ ] User profile customization
- [ ] Advanced search filters
- [ ] Real-time notifications
- [ ] Mobile responsive design
- [ ] API documentation (Swagger)
- [ ] Unit test coverage
- [ ] Docker containerization
