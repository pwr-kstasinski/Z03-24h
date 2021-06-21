from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI, jsonapi_rpc
from sqlalchemy import create_engine
import sqlite3


db = SQLAlchemy()
messages = {'allchat' : []} #{'user': [mess1, mess2, ...]}
accounts_data = {} #{'username': 'password', ...}
grp_chat = {} 
class Server(SAFRSBase, db.Model):
    '''
    description: Message
    '''

    __tablename__ = "Server"
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def get_messages_addressed_to(self, username, save=False):
        '''
        description: Get message
        args:
            username: "pawel0110"
        '''
        mess = []
        
        if username in messages:
            mess = messages[username]
            if save==False:
                messages[username] = []
                try:
                    sqliteConnection = sqlite3.connect('sqlite.db')
                    cursor = sqliteConnection.cursor()
    
                    sql = "DELETE FROM messages WHERE login = '" + username + "'"        
                    cursor.execute(sql)
                    sqliteConnection.commit()    
                    cursor.close()
                except sqlite3.Error as error:
                    print("Failed to insert Python variable into sqlite table", error)
                finally:
                    if (sqliteConnection):
                        sqliteConnection.close()
                    print("The SQLite connection is closed")
            return {'result': mess}

    @classmethod
    @jsonapi_rpc(http_methods=["GET"])
    def get_messages_from_grpchat(self):
        '''
        description: Get messages from grpchat
        '''
        mess = {}
        for username in grp_chat:
            mess[username]=grp_chat[username]
        conn = sqlite3.connect('sqlite.db')
        cur = conn.cursor()
        all_users = cur.execute('SELECT * FROM messages WHERE fromUser=\'allchat\'').fetchall()
        return {'result': mess}

    @classmethod
    @jsonapi_rpc(http_methods=["GET"])
    def get_all_users(self):
        '''
        description: Get all users
        '''
        all_users = []
        for username in messages:
            all_users.append(username)
        return {'result': all_users}
    

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
        try:
            sqliteConnection = sqlite3.connect('sqlite.db')
            cursor = sqliteConnection.cursor()
        
            sqlite_insert_with_param = """INSERT INTO messages
                        (fromUser, toUser, msg) 
                        VALUES (?, ?, ?);"""
    
            data_tuple = (msg["sender"], msg["receiver"], msg["content"])
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()    
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
        if rec == 'allchat':
            grp_chat[sen]=[msg]
            return {'result': 'success'}
        if not rec in messages.keys():
            messages[rec] = [msg]
        else:
            messages[rec].append(msg)

        return {'result': 'success'}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def log_in_user(self, user_name, password):
        '''
                description: log in user
                args:
                    user_name: "pawel0110"
                    password: "1234"
        '''
        if not user_name in messages.keys():
            return {'result': 'failed'}

        if accounts_data[user_name]==password:
            return {'result': 'success'}
        return {'result': 'failed'}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def register_user(self, user_name, password):
        '''
                description: register user
                args:
                    user_name: "pawel0110"
                    password: "1234"
        '''
        if not user_name in messages.keys():
            messages[user_name] = []
            accounts_data[user_name]=password
            return {'result': 'success'}
        try:
            sqliteConnection = sqlite3.connect('sqlite.db')
            cursor = sqliteConnection.cursor()
        
            sqlite_insert_with_param = """INSERT INTO users
                        (login, password) 
                        VALUES (?, ?);"""
    
            data_tuple = (user_name, password)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()    
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

        return {'result': 'failed'}


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
    app.debug = True
    app.run(host=host)


if __name__ == "__main__":
    main()