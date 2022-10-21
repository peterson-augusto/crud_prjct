from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:86518995@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(70), nullable=True)
    l_name = db.Column(db.String(70), nullable=True)
    email = db.Column(db.String(20), unique=True)
    genre = db.Column(db.String(15))
    birthdata = db.Column(db.Date, nullable=True)
    password = db.Column(db.Integer, nullable=True)

    
    def __init__(self, f_name, l_name, email, genre, birthdata, password):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.genre = genre
        self.birthdata = birthdata
        self.password = password

db.create_all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'genre', 'birthdata', 'password')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})



# Cadastro de usuários
@app.route('/register', methods = ['GET', 'POST'])
def create_user():
    f_name = request.json['f_name']
    l_name = request.json['l_name']
    email = request.json['email']
    genre = request.json['genre']
    birthdata = request.json['birthdata']
    password = request.json['password']
        
    new_user = User(f_name, l_name, email, genre, birthdata, password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), render_template('/cadastro.html')


    
@app.route('/users', methods = ['GET'])
def get_users():    
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

    
@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    user = User.query.get(id)
    
    f_name = request.json['f_name']
    l_name = request.json['l_name']
    email = request.json['email']
    genre = request.json['genre']
    birthdata = request.json['birhdata']
    password = request.json['password']
    
    user.f_name = f_name
    user.l_name = l_name
    user.email = email
    user.genre = genre
    user.birthdata = birthdata
    user.password = password
        
    db.session.commit()
    return user_schema.jsonify(user)
        
@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
    
    
    


