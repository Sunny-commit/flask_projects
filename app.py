
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lost_and_found.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Dynamic storage for reported items
class ReportedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    reported_by = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    date = db.Column(db.String(100), nullable=False)
    proof = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<ReportedItem {self.item_name}>"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_lost = ReportedItem.query.filter_by(status='Lost').count()
    total_found = ReportedItem.query.filter_by(status='Found').count()
    recent_activity = ReportedItem.query.order_by(ReportedItem.date.desc()).limit(5).all()

    data = {
        "total_lost": total_lost,
        "total_found": total_found,
        "recent_activity": recent_activity,
    }
    return render_template('dashboard.html', data=data)

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        status = request.form['status']
        address = request.form['address']
        file = request.files['proof']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_item = ReportedItem(
                item_name=item_name,
                description=description,
                status=status,
                reported_by="Anonymous",
                address=address,
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                proof=filename
            )

            db.session.add(new_item)
            db.session.commit()

            flash('Report submitted successfully!', 'success')

            # Redirect to the dashboard after the report is submitted
            return redirect(url_for('dashboard'))  # This will redirect to the dashboard page

    return render_template('report.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))

if __name__ == '__main__':
    app.run(debug=True)