from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lost_and_found.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reported_by = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Lost")
    proof = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

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

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', item=item)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
