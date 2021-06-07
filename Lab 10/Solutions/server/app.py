import json

from flask import Flask, jsonify, request, make_response
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
import jwt
import datetime
from functools import wraps
from flask_socketio import SocketIO, ConnectionRefusedError, disconnect, join_room

from datebase import User, Message, Group
from tools import auth_tools, group_tools, message_tools, user_tools, chat_tools
from tools.alchemy_encoder import new_alchemy_encoder, FlatAlchemyEncoder

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mOj-SuPeR-UlTrA-SeCrEt-K3y'
app.config['SERVER'] = '127.0.0.1'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auth_tools.init_bcrypt(app)
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
        socketio.emit('register_new_chat', 'res', broadcast=True)
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
    user_id = None
    try:
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        group = data['group']
        user_id = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])['id']
    except:
        return make_response('Invalid args', 400)

    message_list = message_tools.get_group_messages(receiver_id) if group else message_tools.get_messages(sender_id,
                                                                                                          receiver_id)
    # unread = message_tools.get_unread_messages(user_id)
    unread = message_tools.get_all_unread_messages()

    unread = list(map(lambda a: a[1], unread))

    for mess in message_list:
        mess.unread = mess.id in unread
    # for mess in message_list:
    #     mess.unread = (user_id, mess.id) in unread

    # return json.dumps(message_list, cls=new_alchemy_encoder(False, ['unread']), check_circular=False)
    return json.dumps(message_list, cls=FlatAlchemyEncoder)


@app.route('/message', methods=['POST'])
@cross_origin()
@token_required
def send_messages_route():
    """
    swagger_from_file: docs/message-post.yml
    """
    data = request.get_json()
    try:
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        message = data['message']
        group = data['group']
    except Exception as e:
        return make_response('Invalid args', 400)

    res = message_tools.add_message(Message(sender_id, receiver_id, message, group))

    if res:
        room = ''
        if group:
            room = f'group{receiver_id}'
        else:
            receiver_id = int(receiver_id)
            if receiver_id in users:
                room = users[int(receiver_id)]

        if receiver_id == 0:
            socketio.emit('read_message', res, broadcast=True)
        else:
            socketio.emit('read_message', res, room=room)

        return jsonify(''), 200
    else:
        return make_response('Error', 400)


@app.route('/message/status', methods=['PUT'])
@cross_origin()
@token_required
def update_message_status_route():
    """
    swagger_from_file: docs/message-status.yml
    """
    user_id = 0
    data = request.get_json()
    try:
        user_id = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])['id']
    except:
        return make_response('Invalid args', 400)

    res = message_tools.update_messages_status(data, user_id)

    if res:
        mess: Message = message_tools.get_message_by_id(data[0])
        room = ''
        if mess.group:
            room = f'group{mess.receiver_id}'
        else:
            room = users[mess.sender_id]

        res = {'message_id': data, 'user_id': user_id, 'group': mess.group, 'group_id': mess.receiver_id}

        if mess.receiver_id == 0:
            socketio.emit('read_message', res, broadcast=True)
        else:
            socketio.emit('read_message', res, room=room)

        return jsonify(''), 200


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
    return json.dumps(data, cls=FlatAlchemyEncoder)


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
        owner_id = data['owner_id']
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


@app.route('/chat-list', methods=['GET'])
@cross_origin()
@token_required
def get_chat_list_route():
    """
    swagger_from_file: docs/chat-list.yml
    """
    try:
        user_id = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])['id']
    except:
        return make_response('Invalid args', 400)

    chat_list = chat_tools.get_chat_list(user_id)

    return json.dumps(chat_list, cls=new_alchemy_encoder(False, ['message']), check_circular=False)


@app.route('/spec')
def spec_route():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Messenger API'
    return jsonify(swag)


@socketio.on('connect')
def connSocket():
    try:
        data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
    except:
        disconnect(sid=request.sid)
        raise ConnectionRefusedError('unauthorized!')
    print('connect')
    if 'user' in data:
        user_id = data['id']
        users[user_id] = request.sid
        sids[request.sid] = user_id
        update_status(user_id, True)

        list = group_tools.get_user_group(data['id'])
        for (group_id, _) in list:
            join_room(f'group{group_id}')

    else:
        disconnect(sid=request.sid)


@socketio.on('disconnect')
def disc():
    login = sids[request.sid]
    update_status(login, False)
    del sids[request.sid]
    del users[login]


def update_status(user_id: int, online: bool):
    socketio.emit('status', {'user_id': user_id, 'online': online}, broadcast=True)


if __name__ == "__main__":
    # socketio.run(app, log_output=True, debug=True, host='127.0.0.1', port=5000)
    socketio.run(app, host='127.0.0.1', port=5000)
