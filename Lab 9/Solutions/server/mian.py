from datetime import timedelta
import datetime
from flask import Flask, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqllite3'
app.secret_key = "SUPER_secreet_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

class users(db.Model):
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column("passwd", db.String(20))

    def to_dict(self):
        return {"name": self.username}

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class Message(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True, autoincrement = True)
    sender = db.Column(db.String(20), db.ForeignKey(users.username))
    content = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #room_target = db.Column(db.Integer, db.ForeignKey(Room._id), nullable = True)
    user_target = db.Column(db.String(20), db.ForeignKey(users.username), nullable = True)
    brodcast = db.Column(db.Boolean)

    def to_dict(self):
        return {"sender": self.sender, "content": self.content,"time": self.creation_date}

    def __init__(self, sender, content, brodcast = False,room_target = None, user_target = None) -> None:
        self.sender = sender
        self.content = content
        self.brodcast = brodcast
        #self.room_target = room_target
        self.user_target = user_target


db.create_all()
# db.session.add(Message("Jan1","YEEEEE", user_target="test"))
# db.session.commit()

@app.route('/pong', methods = ["GET"])
def pong():
    if 't' in session:
        session.clear()
        return f"pong session",200
    session["t"] = "YEE"
    return "pong",200

@app.route("/create_account", methods = ["POST"])
def createAccount():
    content = request.json
    usr_name = content["usr_name"].strip()
    passwd = content["passwd"]

    users_found = users.query.filter_by(username = usr_name).first()
    if users_found:
        return {"status": "fail","message": "This username is already exist"}, 409

    usr = users(usr_name,passwd)
    db.session.add(usr)
    db.session.commit()

    return {"status": "succes","message": "Account created"}, 201

@app.route("/login", methods = ["POST"])
#@cross_origin(origin='*')
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

@app.route("/recive/<username>", methods = ["GET"])
def getMessages(username):
    # to przydało by się lepiej roziązać
    # middleware było by pomocne
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    messages = Message.query.filter(or_(
        and_(Message.sender == session["username"], Message.user_target == username),
        and_(Message.sender == username, Message.user_target == session["username"]))
        ).order_by(Message.creation_date)
    out = list(map(Message.to_dict,messages))

    return {"status": "succes", "messages": out}, 200


@app.route("/users", methods = ["GET"])
def getUsers():
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    all_users = users.query.filter(users.username != session['username']).all()
    all_users = list(map(users.to_dict,all_users))

    return {"status": "succes", "users": all_users}, 200


@app.route("/send", methods = ["POST"])
def sendMessage():
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    content = request.json
    target = content["target"]
    content = content["content"]
    sender = session['username']

    target_usr = users.query.filter_by(username = target).first()

    # iiny kod błędu
    if not target_usr:
        return {"status": "fail", "message": f"No such user"}, 401

    msg = Message(sender, content, user_target=target_usr.username)
    db.session.add(msg)
    db.session.commit()

    return {"status": "succes", "message": f""}, 201


@app.route("/brodcast", methods = ["POST","GET"])
def brodcastSendMsg():
    if not 'username' in session:
            return {"status": "fail", "message": f"You need to log in first"}, 401

    if request.method == "POST":
        content = request.json
        content = content["content"]
        sender = session['username']

        msg = Message(sender, content, brodcast=True)
        db.session.add(msg)
        db.session.commit()

        return {"status": "succes", "message": f""}, 201
        
    if request.method == "GET":
        messages = Message.query.filter_by(brodcast = True).order_by(Message.creation_date).all()
        out = list(map(Message.to_dict,messages))
        return {"status": "succes", "messages": out}, 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
