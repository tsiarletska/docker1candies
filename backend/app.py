from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class CandyType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    candies = db.relationship('Candy', backref='type', lazy=True)

class Candy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    type_id = db.Column(db.Integer, db.ForeignKey('candy_type.id'), nullable=False)

# Routes
@app.route('/api/candies', methods=['GET'])
def get_candies():
    candies = Candy.query.all()
    return jsonify([{
        'id': candy.id,
        'name': candy.name,
        'price': candy.price,
        'description': candy.description,
        'type': candy.type.name
    } for candy in candies])

@app.route('/api/types', methods=['GET'])
def get_types():
    types = CandyType.query.all()
    return jsonify([{
        'id': type.id,
        'name': type.name
    } for type in types])

# Initialize database and add sample data
def init_db():
    with app.app_context():
        db.create_all()

        # Check if we already have data
        if CandyType.query.first() is None:
            # Add candy types
            chocolate = CandyType(name='Chocolate')
            gummy = CandyType(name='Gummy')
            hard_candy = CandyType(name='Hard Candy')

            db.session.add_all([chocolate, gummy, hard_candy])
            db.session.commit()

            # Add candies
            candies = [
                Candy(name='Dark Chocolate Bar', price=2.99,
                     description='Rich dark chocolate bar', type_id=chocolate.id),
                Candy(name='Milk Chocolate Bar', price=2.49,
                     description='Creamy milk chocolate bar', type_id=chocolate.id),
                Candy(name='Gummy Bears', price=1.99,
                     description='Fruity gummy bears', type_id=gummy.id),
                Candy(name='Gummy Worms', price=1.99,
                     description='Sour gummy worms', type_id=gummy.id),
                Candy(name='Lollipop', price=0.99,
                     description='Classic cherry lollipop', type_id=hard_candy.id),
            ]

            db.session.add_all(candies)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=3001)
