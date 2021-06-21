import json

from flask import Flask, jsonify, request, make_response, Response
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
import jwt
import datetime
from functools import wraps
from flask_socketio import SocketIO

from datebase import User, Message, Group
from tools import auth_tools, group_tools, message_tools, user_tools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mOj-SuPeR-UlTrA-SeCrEt-K3y'
app.config['SERVER'] = '127.0.0.1'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auth_tools.init_bcrypt(app)
# socketio = SocketIO(app, logger=True, engineio_logger=True, always_connect=True, async_mode="threading",
#                     cors_allowed_origins="*")
socketio = SocketIO(app, always_connect=True, async_mode="threading", cors_allowed_origins="*")

users = {}
sids = {}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            token = request.args.get('token')
            if not token:
                return jsonify({'message': 'Token is missing'}), 403
        except:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)

    return decorated


@app.route('/login', methods=['POST'])
@cross_origin()
def login_route():
    """
    swagger_from_file: docs/login.yml
    """
    auth = request.get_json()
    if auth_tools.check_login(User(auth['login'], auth['password'])):
        user: User = user_tools.get_user_by_name(auth['login'])
        if not user:
            make_response('Bad request', 400)
        token = jwt.encode({
            'id': user.id,
            'user': user.login,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Invalid user or password', 401)


@app.route('/register', methods=['POST'])
@cross_origin()
def register_route():
    """
    swagger_from_file: docs/register.yml
    """
    auth = request.get_json()
    user = User(auth['login'], auth['password'])
    if not auth_tools.is_login_free(user):
        return make_response('Login exists', 409)
    if auth_tools.register_user(user):
        return jsonify('Ok'), 201

    return make_response('Something went wrong', 400)


@app.route('/message-list', methods=['POST'])
@cross_origin()
@token_required
def get_message_list_route():
    """
    swagger_from_file: docs/message-list-post.yml
    """

    data = request.get_json()
    try:
        sender_id = data['senderId']
        receiver_id = data['receiverId']
        group = data['group']
    except:
        return make_response('Invalid args', 400)

    message_list = message_tools.get_group_messages(receiver_id) if group else message_tools.get_messages(sender_id,
                                                                                                          receiver_id)
    data = []

    for mess in message_list:
        data.append({
            'id': mess.id,
            'senderId': mess.sender_id,
            'receiverId': mess.receiver_id,
            'message': mess.message,
            'group': mess.group,
            'date': mess.date
        })

    return jsonify(data=data)


@app.route('/message', methods=['POST'])
@cross_origin()
@token_required
def send_messages_route():
    """
    swagger_from_file: docs/message-post.yml
    """
    data = request.get_json()
    try:
        sender_id = data['senderId']
        receiver_id = data['receiverId']
        message = data['message']
        group = data['group']
    except:
        return make_response('Invalid args', 400)

    res = message_tools.add_message(Message(sender_id, receiver_id, message, group))

    if res:
        return jsonify(''), 200
    else:
        return make_response('Error', 400)


@app.route('/users', methods=['GET'])
@cross_origin()
@token_required
def get_users_route():
    """
    swagger_from_file: docs/user-get.yml
    """
    data = []
    users_list = user_tools.get_users()
    for u in users_list:
        data.append({
            'id': u.id,
            'login': u.login
        })
    return jsonify(data=data)


@app.route('/groups', methods=['GET'])
@cross_origin()
@token_required
def get_groups_route():
    """
    swagger_from_file: docs/group-get.yml
    """
    return jsonify(group_tools.get_groups()), 200


@app.route('/groups', methods=['POST'])
@cross_origin()
@token_required
def create_group_route():
    """
    swagger_from_file: docs/group-post.yml
    """
    data = request.get_json()
    try:
        name = data['name']
        owner_id = data['ownerId']
    except:
        return make_response('Invalid args', 400)

    res = group_tools.add_group(Group(name, owner_id))
    if res:
        return jsonify(f'Added group {name}'), 201
    else:
        return make_response('Bad request', 400)


@app.route('/online', methods=['GET'])
@cross_origin()
@token_required
def get_online_users():
    """
    swagger_from_file: docs/status.yml
    """
    return jsonify([*users.keys()])


@app.route('/spec')
def spec_route():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Messenger API'
    return jsonify(swag)


@socketio.on('auth')
def conn(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return
    if 'user' in data:
        login = data['user']
        users[login] = request.sid
        sids[request.sid] = login
        update_status(login, True)


@socketio.on('disconnect')
def disc():
    login = sids[request.sid]
    update_status(login, False)
    del sids[request.sid]
    del users[login]


def update_status(login: str, online: bool):
    socketio.emit('status', {'login': login, 'online': online}, broadcast=True)


if __name__ == "__main__":
    # socketio.run(app, log_output=True, debug=True, host='127.0.0.1', port=5000)
    socketio.run(app, host='127.0.0.1', port=5000)
