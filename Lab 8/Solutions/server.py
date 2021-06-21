from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI, jsonapi_rpc
from sqlalchemy import create_engine

db = SQLAlchemy()
messages = {} #{'user': [mess1, mess2, ...]}

class Server(SAFRSBase, db.Model):
    '''
    description: Message
    '''

    __tablename__ = "Server"
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def get_messages_addressed_to(self, username):
        '''
        description: Get message
        args:
            username: "pawel0110"
        '''
        mess = []
        if username in messages:
            mess = messages[username]
            messages[username] = []
        return {'result': mess}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def send_message(self, **kwargs):
        '''
            description: Send message
            args:
                sender: "Grzegorz"
                receiver: "Mariusz"
                msg_content: "hello"
        '''
        sen = kwargs.get('sender')
        rec = kwargs.get('receiver')
        mess_con = kwargs.get('msg_content')
        print(kwargs.get('sender'))
        print(kwargs.get('receiver'))
        print(kwargs.get('msg_content'))
        msg = {'receiver': kwargs.get('receiver'), 'sender': kwargs.get('sender'), 'content': kwargs.get('msg_content')}

        if not rec in messages.keys():
            messages[rec] = [msg]
        else:
            messages[rec].append(msg)

        return {'result': 'success'}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def login_or_register_user(self, user_name):
        '''
                description: login or register user
                args:
                    user_name: "pawel0110"
        '''
        if not user_name in messages.keys():
            messages[user_name] = []

        return {'result': 'success'}


def create_api(app, HOST="localhost", PORT=5000, API_PREFIX="", schemes=["http"]):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(Server)
    print("Starting API: http://{}:{}/{}".format(HOST, PORT, API_PREFIX))


def create_app(config_filename=None, host="localhost"):
    app = Flask("app")
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite://')
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_api(app, host)
    return app


host = 'localhost'
app = create_app(host=host)


def main():
    app.run(host=host)


if __name__ == "__main__":
    main()