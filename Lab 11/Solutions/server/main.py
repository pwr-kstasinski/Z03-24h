from datetime import timedelta
import datetime
from flask import Flask, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, func, desc, create_engine, Column, ForeignKey, Integer, String, DATETIME, Boolean
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, namespace
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import user

db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'example')
db_host = os.getenv('DB_HOST', '0.0.0.0')
db_port = os.getenv('DB_PORT', '3306')

# database connection
# mariadb+mariadbconnector://app_user:Password123!@127.0.0.1:3306/company
# "mariadb+mariadbconnector://{}:{}@{}:{}".format(
#    db_user, db_password, db_host, db_port)
engine = create_engine(
    "mariadb+mariadbconnector://{}:{}@{}:{}".format(
        db_user, db_password, db_host, db_port)
)
engine.execute(r"CREATE DATABASE IF NOT EXISTS messenger")
engine.execute(r"USE messenger")
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# app setup
app = Flask(__name__)
app.secret_key = "SUPER_secreet_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app, supports_credentials=True)

socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")


def getSession():
    engine.execute(r"USE messenger")
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# ====================== dadabase ===================================


class users(Base):
    __tablename__ = "users"
    username = Column(String(20), primary_key=True)
    password = Column("passwd", String(20))
    isActive = Column(Boolean)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.isActive = False


class Message(Base):
    __tablename__ = "Message"
    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    sender = Column(String(20), ForeignKey(users.username))
    content = Column(String(200))
    creation_date = Column(DATETIME, default=datetime.datetime.utcnow)
    user_target = Column(String(20), ForeignKey(
        users.username), nullable=True)
    brodcast = Column(Boolean)
    readed = Column(Boolean, default=False)

    def to_dict(self):
        return {"id": self._id, "sender": self.sender, "content": self.content, "time": self.creation_date, "readed": self.readed}

    def __init__(self, sender, content, brodcast=False, room_target=None, user_target=None, readed=False) -> None:
        self.sender = sender
        self.content = content
        self.brodcast = brodcast
        self.user_target = user_target
        self.readed = readed


Base.metadata.clear()
Base.metadata.create_all(bind=engine, checkfirst=True)
getSession().commit()

# ========================== routes =================================


@app.route('/ping', methods=["GET"])
def pong():
    print("ping -> pong")
    return "pong", 200


@app.route("/create_account", methods=["POST"])
def createAccount():
    content = request.json
    usr_name = content["usr_name"].strip()
    passwd = content["passwd"]

    db = getSession()
    users_found = db.query(users).filter_by(username=usr_name).first()
    if users_found:
        return {"status": "fail", "message": "This username is already exist"}, 409

    usr = users(usr_name, passwd)
    db.add(usr)
    db.commit()

    socketio.emit("reload_userlist", {}, namespace="/")

    return {"status": "succes", "message": "Account created"}, 201


@app.route("/login", methods=["POST"])
def login():
    content = request.json
    usr_name = content["usr_name"]
    passwd = content["passwd"]

    if 'username' in session:
        return {"status": "succes", "message": f"Yeou are already logged as {usr_name}"}, 200

    db = getSession()
    found_user = db.query(users).filter_by(
        username=usr_name).first()
    if (not found_user) or found_user.password != passwd:
        return {"status": "fail", "message": "Login or password is wrong"}, 401

    session['username'] = found_user.username
    found_user.isActive = True
    db.commit()

    socketio.emit("reload_userlist", {}, namespace="/")

    return {"status": "succes", "message": f"Welcome back {usr_name}"}, 200


@app.route("/logout", methods=["GET"])
def logout():
    db = getSession()
    user = db.query(users).filter_by(username=session["username"]).first()
    user.isActive = False
    db.commit()

    session.clear()
    socketio.emit("reload_userlist", {}, namespace="/")
    return {"status": "succes", "message": f"You are logged out"}, 200


@app.route("/recive/<username>", methods=["GET"])
def getMessages(username):
    # to przydało by się lepiej roziązać
    # middleware było by pomocne
    if not 'username' in session:
        return {"status": "fail", "message": f"You need to log in first"}, 401

    db = getSession()
    messages = db.query(Message).filter(or_(
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

    db = getSession()
    all_users = db.query(users).filter(
        users.username != session['username']).all()

    def usersToDict(user: users):
        new_messages_cont = db.query(Message).filter(
            and_(
                Message.sender == user.username,
                Message.user_target == session["username"],
                Message.readed == False
            )).with_entities(func.count()).scalar()

        recent_activity = db.query(Message).filter(
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

    db = getSession()
    messages = db.query(Message).filter(
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

    db.commit()

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

    db = getSession()
    target_usr = db.query(users).filter_by(username=target).first()

    # iiny kod błędu ?
    if not target_usr:
        return {"status": "fail", "message": f"No such user"}, 401

    msg = Message(sender, content, user_target=target_usr.username)
    db.add(msg)
    db.commit()

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

        db = getSession()
        msg = Message(sender, content, brodcast=True, readed=True)
        db.add(msg)
        db.commit()

        socketio.emit("reload_messages", {}, namespace="/")

        return {"status": "succes", "message": f""}, 201

    if request.method == "GET":
        db = getSession()
        messages = db.query(Message).filter_by(
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
