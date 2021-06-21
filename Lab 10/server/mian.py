from datetime import timedelta
import datetime
from flask import Flask, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, func, desc
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, namespace

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqllite3'
app.secret_key = "SUPER_secreet_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")


# ====================== dadabase ===================================

class users(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column("passwd", db.String(20))
    isActive = db.Column(db.Boolean)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.isActive = False


class Message(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.String(20), db.ForeignKey(users.username))
    content = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_target = db.Column(db.String(20), db.ForeignKey(
        users.username), nullable=True)
    brodcast = db.Column(db.Boolean)
    readed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self._id, "sender": self.sender, "content": self.content, "time": self.creation_date, "readed": self.readed}

    def __init__(self, sender, content, brodcast=False, room_target=None, user_target=None, readed=False) -> None:
        self.sender = sender
        self.content = content
        self.brodcast = brodcast
        self.user_target = user_target
        self.readed = readed


db.create_all()


# ========================== routes =================================

@app.route('/pong', methods=["GET"])
def pong():
    if 't' in session:
        session.clear()
        return f"pong session", 200
    session["t"] = "YEE"
    return "pong", 200


@app.route("/create_account", methods=["POST"])
def createAccount():
    content = request.json
    usr_name = content["usr_name"].strip()
    passwd = content["passwd"]

    users_found = users.query.filter_by(username=usr_name).first()
    if users_found:
        return {"status": "fail", "message": "This username is already exist"}, 409

    usr = users(usr_name, passwd)
    db.session.add(usr)
    db.session.commit()

    socketio.emit("reload_userlist", {}, namespace="/")

    return {"status": "succes", "message": "Account created"}, 201


@app.route("/login", methods=["POST"])
def login():
    content = request.json
    usr_name = content["usr_name"]
    passwd = content["passwd"]

    if 'username' in session:
        return {"status": "succes", "message": f"Yeou are already logged as {usr_name}"}, 200

    found_user = users.query.filter_by(username=usr_name).first()
    if (not found_user) or found_user.password != passwd:
        return {"status": "fail", "message": "Login or password is wrong"}, 401

    session['username'] = found_user.username
    found_user.isActive = True
    db.session.commit()

    socketio.emit("reload_userlist", {}, namespace="/")

    return {"status": "succes", "message": f"Welcome back {usr_name}"}, 200


@app.route("/logout", methods=["GET"])
def logout():
    user = users.query.filter_by(username=session["username"]).first()
    user.isActive = False
    db.session.commit()

    session.clear()
    socketio.emit("reload_userlist", {}, namespace="/")
    return {"status": "succes", "message": f"You are logged out"}, 200


@app.route("/recive/<username>", methods=["GET"])
def getMessages(username):
    # to przydało by się lepiej roziązać
    # middleware było by pomocne
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    messages = Message.query.filter(or_(
        and_(Message.sender == session["username"],
             Message.user_target == username),
        and_(Message.sender == username, Message.user_target == session["username"]))
    ).order_by(Message.creation_date)
    out = list(map(Message.to_dict, messages))

    return {"status": "succes", "messages": out}, 200


@app.route("/users", methods=["GET"])
def getUsers():
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    all_users = users.query.filter(users.username != session['username']).all()

    def usersToDict(user: users):
        new_messages_cont = Message.query.filter(
            and_(
                Message.sender == user.username,
                Message.user_target == session["username"],
                Message.readed == False
            )).with_entities(func.count()).scalar()

        recent_activity = Message.query.filter(
            and_(
                Message.sender == user.username,
                Message.user_target == session["username"],
            )).order_by(desc(Message.creation_date)).first()

        if recent_activity:
            recent_activity = recent_activity.creation_date
        else:
            recent_activity = None

        return {"name": user.username, "new_messages_cont": new_messages_cont, "active": user.isActive, "recent_activity": recent_activity}

    all_users = list(map(usersToDict, all_users))

    return {"status": "succes", "users": all_users}, 200


@app.route("/readed", methods=["POST"])
def setReadedMessages():
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    content = request.json
    message_ids = content["msg_ids"]

    messages = Message.query.filter(
        and_(
            Message._id.in_(message_ids),
            Message.user_target == session["username"],
            Message.readed == False
        )).all()

    for msg in messages:
        msg.readed = True

    who = None
    if len(messages) >= 1:
        who = messages[0].sender

    db.session.commit()

    socketio.emit("reload_userlist", {
        "who": session["username"]}, namespace="/")

    if who:
        socketio.emit("reload_messages", {
            "who":  session["username"], "from": who}, namespace="/")
        socketio.emit("reload_messages", {
            "who":  who, "from": session["username"]}, namespace="/")

    return {"status": "succes", "message": f""}, 201


@app.route("/send", methods=["POST"])
def sendMessage():
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    content = request.json
    target = content["target"]
    content = content["content"]
    sender = session['username']

    target_usr = users.query.filter_by(username=target).first()

    # iiny kod błędu ?
    if not target_usr:
        return {"status": "fail", "message": f"No such user"}, 401

    msg = Message(sender, content, user_target=target_usr.username)
    db.session.add(msg)
    db.session.commit()

    socketio.emit("reload_messages", {
                  "who": target_usr.username, "from": session["username"]}, namespace="/")
    socketio.emit("reload_userlist", {
                  "who": target_usr.username, "from": session["username"]}, namespace="/")

    return {"status": "succes", "message": f""}, 201


@app.route("/brodcast", methods=["POST", "GET"])
def brodcastSendMsg():
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    if request.method == "POST":
        content = request.json
        content = content["content"]
        sender = session['username']

        msg = Message(sender, content, brodcast=True, readed=True)
        db.session.add(msg)
        db.session.commit()

        socketio.emit("reload_messages", {}, namespace="/")

        return {"status": "succes", "message": f""}, 201

    if request.method == "GET":
        messages = Message.query.filter_by(
            brodcast=True).order_by(Message.creation_date).all()
        out = list(map(Message.to_dict, messages))
        return {"status": "succes", "messages": out}, 200


# ========================== sockets =================================

@socketio.on('connect')
def connect():
    print('================ Client connected ', session.get("userneme", "---"))


@socketio.on('disconnect')
def disconnect():
    print('>>>>>>>>>>>=============== Client disconnected ',
          session.get("userneme", "---"))


if __name__ == '__main__':
    socketio.run(app, debug=True)
