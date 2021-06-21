from flask import Flask, jsonify, request, make_response
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
import jwt
import datetime
from functools import wraps

from tools import valid_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mOj-SuPeR-UlTrA-SeCrEt-K3y'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


messages = []


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
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(data, *args, **kwargs)

    return decorated


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    """
    swagger_from_file: docs/login.yml
    """
    auth = request.get_json()
    if valid_user(auth['login'], auth['password']):
        token = jwt.encode({'user': auth['login'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Invalid user or password', 401)


@app.route('/message', methods=['GET'])
@cross_origin()
@token_required
def get_message(token_data):
    """
    swagger_from_file: docs/message-get.yml
    """
    return jsonify(messages)


@app.route('/message', methods=['POST'])
@cross_origin()
@token_required
def send_messages(token_data):
    """
    swagger_from_file: docs/message-post.yml
    """
    data = request.get_json()
    print(data)
    if not data or not data['message']:
        return make_response('Bad request', 400)
    else:
        messages.append({'message': data['message'], 'sender': token_data['user'], 'receiver': data['receiver']})
        return ''


@app.route('/spec')
def spec():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Messenger API'
    return jsonify(swag)


if __name__ == "__main__":
    app.run(debug=True)
