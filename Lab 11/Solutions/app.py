from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash

import os
from wtforms_fields import *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, UserMixin
from flask_socketio import SocketIO, send
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    os.environ['USER'], os.environ['PASSWORD'], os.environ['HOST'], os.environ['DB']
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

socketio = SocketIO(app)

login = LoginManager(app)

login.init_app(app)
migrate = Migrate(app, db)

activeUsers = []


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    status = db.Column(db.Boolean, default=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(25), nullable=False)
    user2 = db.Column(db.String(25), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idChat = db.Column(db.Integer)
    idAuthor = db.Column(db.String(25), nullable=False)
    wasRead = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default=datetime.now)
    text = db.Column(db.String(100), nullable=False)


@login.user_loader
def load_user(id):
    if User.query.get(id):
        activeUsers.append(User.query.get(id).username)
    return User.query.get(id)


def chatUnreadMessages(id):
    i = 0
    for m in Message.query.filter_by(idChat=id):
        if m.wasRead == False and m.idAuthor != current_user.username:
            i += 1
    return i


def chatLastMessages(id):
    i = Message.query.filter_by(idChat=id)
    if i:
        result = None
        for m in i:
            result = m.date.strftime("%d.%m.%Y %H:%M:%S")
        if result == None:
            return None
        return "Last message was sent on : " + result
    return None


def findUserChat(idUser1, idUser2):
    first = Chat.query.filter_by(user1=idUser1)
    other = Chat.query.filter_by(user1=idUser2)
    if first:
        for ch in first:
            if ch.user2 == idUser2:
                return ch
    if other:
        for ch in other:
            if ch.user2 == idUser1:
                return ch
    return None


def chatPanel():
    chats = []
    i = 0

    for ch in Chat.query.all():
        if ch.user1 == current_user.username:
            lastMessageTime = chatLastMessages(ch.id)
            unreadMessages = 'No new messages'
            if chatUnreadMessages(ch.id) != 0:
                unreadMessages = "," + str(chatUnreadMessages(ch.id)) + " not displayed messages,"

            isActive = 'Not Active'
            if ch.user2 in activeUsers:
                isActive = 'Active'

            chats.append((ch.user2, lastMessageTime, unreadMessages,
                          isActive, ch.id))
        if ch.user2 == current_user.username:
            lastMessageTime = chatLastMessages(ch.id)
            unreadMessages = 'No new messages'
            if chatUnreadMessages(ch.id) != 0:
                unreadMessages = "," + str(chatUnreadMessages(ch.id)) + " not displayed messages,"

            isActive = 'Not Active'
            if ch.user1 in activeUsers:
                isActive = 'Active'

            chats.append((ch.user1, lastMessageTime, unreadMessages,
                          isActive, ch.id))
    sortedChats = []
    for ch in chats:
        if ch[3] == 'Active':
            sortedChats.append(ch)
    for ch in chats:
        if ch[3] != 'Active':
            sortedChats.append(ch)

    chats = sortedChats
    return chats


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    print()
    user = User.query.filter_by()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        rpassword = reg_form.confirm_password.data
        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password) and pbkdf2_sha256.verify(rpassword, user.password):
            return redirect(url_for('login'))
        if user:
            return "Username is taken! Try another"

        hash_password = pbkdf2_sha256.hash(password)
        u = User(username=username, password=hash_password)
        db.session.add(u)
        db.session.commit()
        flash('Registered succesfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_obj = User.query.filter_by(username=username).first()
        if not user_obj:
            raise ValueError()
        elif not pbkdf2_sha256.verify(password, user_obj.password):
            raise ValueError()

        login_user(user_obj)
        if not current_user.is_authenticated:
            return 'Nope'

        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    chatList = chatPanel()
    chat_form = ChatForm()
    if chat_form.validate_on_submit():
        user = chat_form.user.data
        user_obj = User.query.filter_by(username=user).first()
        if user_obj:
            if findUserChat(current_user.username, user):
                return redirect(url_for('userchat', id_chatu=findUserChat(current_user.username, user).id))
            else:
                if Chat.query.filter_by(user1=current_user.username, user2=user).first() or Chat.query.filter_by(
                        user1=user, user2=current_user.username).first():
                    return "1,5 Arbuza"
                else:
                    if current_user.username < user:
                        c = Chat(user1=current_user.username, user2=user)
                        db.session.add(c)
                        db.session.commit()
                        return redirect(url_for('userchat', id_chatu=c.id))
                    elif current_user.username > user:
                        c = Chat(user1=user, user2=current_user.username)
                        db.session.add(c)
                        db.session.commit()
                        return redirect(url_for('userchat', id_chatu=c.id))
        else:
            return redirect(url_for('chat'))
    return render_template("chat.html", username=current_user.username, form=chat_form, chat=chatList)


@app.route("/userchat/<int:id_chatu>", methods=['GET', 'POST'])
def userchat(id_chatu):
    msg_form = MsgForm()
    wasReadString = ''
    msg_l = Message.query.filter_by(idChat=id_chatu).all()
    msg_list = []
    if msg_form.validate_on_submit():
        text = msg_form.msg.data
        m = Message(idChat=id_chatu, idAuthor=current_user.username,
                    wasRead=False, text=text)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('userchat', id_chatu=id_chatu))

    for msg in msg_l:
        if msg.wasRead:
            wasReadString = 'Displayed'
        else:
            wasReadString = 'Not Displayed'
        msg_list.append(
            (msg.idAuthor, msg.text, wasReadString, ', Sent on : ' + msg.date.strftime("%d.%m.%Y %H:%M:%S")))
        if not msg.wasRead and msg.idAuthor != current_user.username:
            msg.wasRead = True
            db.session.commit()

    chat = Chat.query.filter_by(id=id_chatu).first()
    if chat.user1 == current_user.username:
        return render_template("chats.html", username=current_user.username, user2=chat.user2, msg_form=msg_form,
                               msg=msg_list)
    return render_template("chats.html", username=current_user.username, user2=chat.user1, msg_form=msg_form,
                           msg=msg_list)


@socketio.on('connect')
def connect():
    print('Client connected')


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    send(message)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
