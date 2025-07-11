from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lost_and_found.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reported_by = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Lost")
    proof = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)

# Route for Home Page (Dashboard)
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# Route for Reporting a Lost Item
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        reported_by = request.form['reported_by']
        contact_info = request.form['contact_info']
        proof = request.form['proof']
        address = request.form['address']

        new_item = Item(
            item_name=item_name,
            description=description,
            reported_by=reported_by,
            contact_info=contact_info,
            proof=proof,
            address=address
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('report.html')

# Route for Updating the Item Status
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', item=item)

# Ensure the database tables are created within the application context
if __name__ == '__main__':
    # Wrap the database creation in an app context
    with app.app_context():  # Explicitly create the app context here
        db.create_all()  # Create tables in the database
    app.run(debug=True)


@app.before_first_request
def create_sample_data():
    if not Item.query.first():  # Check if there are no items in the database
        sample_item = Item(
            item_name="Lost Wallet",
            description="A black leather wallet with cash and cards.",
            reported_by="Jane Smith",
            contact_info="jane.smith@example.com",
            status="Lost",
            proof=None,
            address="Building B, Room 202"
        )
        db.session.add(sample_item)
        db.session.commit()

