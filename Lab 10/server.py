from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI, jsonapi_rpc
from datetime import datetime as dt
from flask_socketio import SocketIO


db = SQLAlchemy()


class Message(SAFRSBase, db.Model):
    """
    description: This is Message
    """

    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.String)
    sender = db.Column(db.String)
    content = db.Column(db.String)
    read = db.Column(db.Boolean)
    date_time = db.Column(db.DateTime(timezone=False))

    @classmethod
    @jsonapi_rpc(http_methods=["GET"])
    def get_messages_addressed_to(cls, **kwargs):
        """
        description: Get message
        args:
            receiver_name: receiver name
        """
        messages = {'id': [], 'rec': [], 'sen': [], 'cont': []}
        # messages = {} #{'sender1': [mess11, mess12,..], 'sender2': [mess21, mess22, ...], ...}
        rec_name = kwargs['receiver_name']
        messages_to_receiver = db.session.query(Message).filter_by(receiver=rec_name).all()

        for mess in messages_to_receiver:
            messages['id'].append(mess.id)
            messages['rec'].append(mess.receiver)
            messages['sen'].append(mess.sender)
            messages['cont'].append(mess.content)

        return {'result': messages}

    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def mark_as_seen(cls, **kwargs):
        """
        description: Get message
        args:
            id_list: list of ids
            sender: sender
            receiver: receiver
        """
        mess_id = kwargs['id_list']
        sender = kwargs['sender']
        receiver = kwargs['receiver']
        for mid in mess_id:
            message_to_mark = db.session.query(Message).filter_by(id=mid).first()
            if not message_to_mark is None:
                message_to_mark.read = True
                db.session.commit()

        socketio.emit('messages_displayed', {'receiver': receiver, 'sender': sender})
        return {'result': 'success'}

    @classmethod
    @jsonapi_rpc(http_methods=["GET"])
    def get_conversation(cls, **kwargs):
        """
        description: Get conversation
        args:
            receiver_name: receiver name
        """
        messages = {'id': [], 'rec': [], 'sen': [], 'cont': [], 'dtime': [], 'read': []}
        # messages = {} #{'sender1': [mess11, mess12,..], 'sender2': [mess21, mess22, ...], ...}
        rec_name = kwargs['receiver_name']

        messages_to_receiver = db.session.query(Message).\
            filter( (Message.receiver == rec_name) | (Message.receiver == 'global') | (Message.sender == rec_name) ).all()

        for mess in messages_to_receiver:
            messages['id'].append(mess.id)
            messages['rec'].append(mess.receiver)
            messages['sen'].append(mess.sender)
            messages['cont'].append(mess.content)
            messages['dtime'].append(mess.date_time)
            messages['read'].append(mess.read)

        return {'result': messages}

    @classmethod
    @jsonapi_rpc(http_methods=["GET"])
    def get_number_of_unread_messages(cls, **kwargs):
        """
        description: Get number of unread messages
        args:
            receiver_name: receiver name
            sender_name: sender name
        """
        rec_name = kwargs['receiver_name']
        sen_name = kwargs['sender_name']
        unread_messages = db.session.query(Message).filter_by(receiver=rec_name, sender=sen_name, read=False).all()
        number_of_messages = len(unread_messages)

        return {'result': number_of_messages}


class User(SAFRSBase, db.Model):
    """
        description: User definition
    """

    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    is_online = db.Column(db.Boolean)

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def send_message(cls, **kwargs):
        """
            description: Send message
            args:
                sender: "Grzegorz"
                receiver: "Mariusz"
                msg_content: "hello!"
        """
        receiver = kwargs.get('receiver')
        sender = kwargs.get('sender')
        content = kwargs.get('msg_content')
        msg = Message(receiver=receiver, sender=sender, content=content,
                      read=False, date_time=dt.now())

        db.session.add(msg)
        db.session.commit()
        socketio.emit('new_message', {'receiver': receiver, 'sender': sender})

        return {'result': 'success'}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def login(cls, user_name, user_password):
        """
            description: Register or login user
            args:
                user_name: "username"
                user_password: "password"
        """
        user = db.session.query(User).\
            filter_by(name=user_name, password=user_password).first()

        if user is None:
            return {'result': 'bad_credentials'}
        else:
            user.is_online = True
            db.session.commit()
            socketio.emit('login_or_register')
            return {'result': 'logged_in', 'user_data': {'id': user.id}}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def register(cls, user_name, user_password):
        """
            description: Register or login user
            args:
                user_name: "username"
                user_password: "password"
        """
        user = db.session.query(User).filter_by(name=user_name).first()

        if user is None:
            user = User(name=user_name, password=user_password, is_online=True)
            db.session.add(user)
            db.session.commit()
            socketio.emit('login_or_register')
            return {'result': 'registered', 'user_data': {'id': user.id}}
        else:
            return {'result': 'nickname_in_use'}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def disconnect_user(cls, user_name):
        """
            description: Register or login user
            args:
                user_name: "pawel0110"
                status: False
        """
        user = db.session.query(User).filter_by(name=user_name).first()
        if user is not None:
            user.is_online = False
            db.session.commit()
            socketio.emit('login_or_register')
            return {'result': 'success'}
        else:
            return {'result': 'failure'}


def create_api(app, HOST="localhost", PORT=5000, API_PREFIX=""):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(Message)
    api.expose_object(User)
    user = User(name="Piotrek", password="123", is_online=True)
    print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))


def create_app(config_filename=None, host="localhost"):
    app = Flask("demo_app")
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///minichat.db')
    app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)
    db.init_app(app)
    SAFRSBase.db_commit = False
    with app.app_context():
        db.create_all()
        create_api(app, host)

    return app


host_name = 'localhost'
server_app = create_app(host=host_name)


#def run_server_app():
    #server_app.run(host=host_name)

host_name = 'localhost'
server_app = create_app(host=host_name)
socketio = SocketIO(server_app)

def main():
    #run_server_app()
    socketio.run(server_app)


if __name__ == "__main__":
    main()