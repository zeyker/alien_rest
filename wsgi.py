import os
from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE")
app.config['JWT_SECRET_KEY'] = 'zeyker' 
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

    def __repr__(self):
        return f"<User {self.username}>"


def format_case (mycase):
    arr = []
    group = []
    open = False
    for letter in mycase:
        if letter == '(':
            open = True
        elif open and letter == ')':
            arr.append(group)
            group = []
            open = False
        if open and letter != '(':
            group.append(letter)
        if open != True and letter != ')':
            arr.append(letter)
    return arr


def count_match(arr, words, len_word):

    counter = 0
    for word in words:
        checker = True
        for i in range( 0,len_word):
            if word[i] not in arr[i]:
                checker = False
                break
        if checker:
            counter += 1
    return counter


def response_creator(cases, words, len_words, n_cases):
    response = []
    for i in range(0, n_cases):
        case_formatted = format_case(cases[i])
        matchs = count_match(case_formatted, words, len_words)
        response.append({"case": i+1 ,"count": matchs})
    return response


@app.route('/', methods=['GET'])
def home():
    return {"message": 'Welcome to the aliens app'}


@app.route('/users', methods=['GET'])
@jwt_required
def get_users():

    users = UsersModel.query.all()
    results = [
        {
            "username": user.username,
            "password": user.password
        } for user in users]

    return {"count": len(results), "users": results}


@app.route('/users', methods=['POST'])
def create_users():

    if request.is_json:
        data = request.get_json()
        username = data['username']
        user = UsersModel.query.filter_by(username=username).first()
        if not user:
            hashed_password = generate_password_hash(data['password'], method='sha256')
            new_user = UsersModel(username=username, password = hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"user {new_user.username} has been created successfully."}
        else:
            return {"message": "Username already exists"}, 400
    else:
        return {"error": "The request payload is not in JSON format"}



@app.route("/alien", endpoint="alien", methods=["POST"])
@jwt_required
def new_alien_message():
    req = request.get_json()
    cases = req.get('cases')
    words = req.get('words')
    config = req.get('config')
    response = response_creator(cases, words, config[0], config[2])
    
    return jsonify(response), 201





@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Not a JSON request"}), 400
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = UsersModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Username doesn't exists"}), 400
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Wrong password"}), 400

    expires = datetime.timedelta(minutes=5)
    access_token = create_access_token(identity=username, expires_delta = expires)
    return jsonify(access_token=access_token), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(logged_in_as = current_user), 200

if __name__ == "__main__":
    app.run()


