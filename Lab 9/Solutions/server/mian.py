from datetime import timedelta
import datetime
from flask import Flask, request, session, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow.decorators import post_load

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqllite3'
app.secret_key = "SUPER_secreet_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class users(db.Model):
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column("passwd", db.String(20))

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class Room(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(20))

    def __init__(self, name) -> None:
        self.name = name

class RoomParticipation(db.Model):
    username = db.Column(db.String(20), db.ForeignKey(users.username), 
                         nullable = False, primary_key = True)
    room_id = db.Column(db.Integer, db.ForeignKey(Room._id), primary_key = True)
    # room = db.relationship("room", db.Integer)

    def __init__(self, username, room_id) -> None:
        self.username = username
        self.room_id = room_id


class Message(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True, autoincrement = True)
    sender = db.Column(db.String(20), db.ForeignKey(users.username))
    content = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    room_target = db.Column(db.Integer, db.ForeignKey(Room._id), nullable = True)
    user_target = db.Column(db.String(20), db.ForeignKey(users.username), nullable = True)

    def to_dict(self):
        return {"sender": self.sender,"usr_target": self.user_target or None, "content": self.content}

    def __init__(self, sender, content, room_target = None, user_target = None) -> None:
        self.sender = sender
        self.content = content
        self.room_target = room_target
        self.user_target = user_target


db.create_all()
# db.session.add(Message("Jan1","YEEEEE", user_target="test"))
# db.session.commit()


@app.route("/create_account", methods = ["POST"])
def createAccount():
    content = request.json
    usr_name = content["usr_name"]
    passwd = content["passwd"]

    users_found = users.query.filter_by(username = usr_name).first()
    if users_found:
        return {"status": "fail","message": "This username is already exist"}, 409

    usr = users(usr_name,passwd)
    db.session.add(usr)
    db.session.commit()

    return {"status": "succes","message": "Account created"}, 201

@app.route("/login", methods = ["POST"])
def login():
    content = request.json
    usr_name = content["usr_name"]
    passwd = content["passwd"]

    if 'username' in session:
        return {"status": "succes", "message": f"Yeou are already logged as {usr_name}"}, 200

    found_user = users.query.filter_by(username = usr_name).first()
    if (not found_user) or found_user.password != passwd:
        return {"status": "fail","message": "Login or password is wrong"}, 401

    session['username'] = found_user.username
    return {"status": "succes", "message": f"Welcome back {usr_name}"}, 200

@app.route("/logout", methods = ["GET"])
def logout():
    session.clear()
    return {"status": "succes", "message": f"You are logged out"}, 200

@app.route("/messages/<username>", methods = ["GET"])
def getMessages(username):
    # to przydało by się lepiej roziązać
    # middleware było by pomocne
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    messages = Message.query.filter(
        (Message.sender == username and Message.user_target == session["username"]) or
         (Message.sender == session["username"] and Message.user_target == username)).all()
    out = list(map(Message.to_dict,messages))
    return {"status": "succes", "messages": out}, 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
