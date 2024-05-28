from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onliner.db'
app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6InVzZXIiLCJpYXQiOjE3MTY4OTA0OTh9.s6Daf4E5PpMEkYc9PQz6DPdcl1928iif5jA0bDTAZmI'
db = SQLAlchemy(app)

class OnlinerItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'OnlinerItem(title="{self.title}", price={self.price}, url="{self.url}")'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            g.user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401

    user = User.query.filter_by(username=auth.username).first()
    if not user or user.password != auth.password:
        return jsonify({'message': 'Could not verify'}), 401

    token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})

@app.route('/scrape', methods=['GET'])
@token_required
def scrape():
    url = 'https://www.onliner.by/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    items = soup.find_all('div', class_='schema-product')

    for item in items:
        title = item.find('span', class_='schema-product__title').text.strip()
        price = float(item.find('span', class_='schema-product__price-value').text.strip().replace(' ', ''))
        link = item.find('a', class_='schema-product__link')['href']

        onliner_item = OnlinerItem(title=title, price=price, url=link)
        db.session.add(onliner_item)

    db.session.commit()
    return 'Data scraped and stored in the database.'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)