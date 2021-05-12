from datetime import datetime, timedelta

from flasgger import Swagger
from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy import and_, or_

from database import db_session, User, UserOnline, Message

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'Messengerify API',
    'uiversion': 3
}
swag = Swagger(app)

messages = {
    ('1a', '3c'): [
        {'sender': '1a', 'content': 'Hi there!'},
        {'sender': '3c', 'content': 'Namaste!'},
    ]
}


class UsersAPI(Resource):
    def post(self):
        """
        Add a new user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            required: true
            description: User's login and password in JSON
            schema:
              id: UserAuth
              properties:
                login:
                  type: string
                password:
                  type: string
        responses:
          201:
            description: New user added successfully
            schema:
              id: UserData
              properties:
                login:
                  type: string
                id:
                  type: integer
        """
        user = User(request.json['login'], request.json['password'])
        db_session.add(user)
        db_session.commit()
        return {'login': user.login, 'id': user.id}, 201

    def get(self):
        """
        List all users
        ---
        tags:
          - users
        responses:
          200:
            description: List of users
            schema:
              type: array
              items:
                schema:
                $ref: '#/definitions/UserData'

        """
        users = []
        for user in User.query.all():
            users.append({'login': user.login, 'id': user.id})
        return users, 200


class OnlineUsersAPI(Resource):
    def post(self):
        """
        Send online heartbeat
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            required: true
            description: User's id in JSON
            schema:
              id: UserId
              properties:
                user_id:
                  type: integer
        responses:
          201:
            description: Heartbeat received
        """
        existing_entry = UserOnline.query.filter(UserOnline.user_id == request.json['user_id']).first()
        if existing_entry:
            existing_entry.last_seen = datetime.now()
        else:
            db_session.add(UserOnline(request.json['user_id'], datetime.now()))
        db_session.commit()
        return 'heartbeat received', 201

    def get(self):
        """
        List all users that are online
        ---
        tags:
          - users
        responses:
          200:
            description: List of users
            schema:
              type: array
              items:
                schema:
                $ref: '#/definitions/UserData'

        """
        users = []
        for user, online in db_session.query(User, UserOnline).filter(and_(User.id == UserOnline.user_id, UserOnline.last_seen > datetime.now() - timedelta(seconds=10))).all():
            users.append({'login': user.login, 'id': user.id, 'last_seen': str(online.last_seen)})
        return users, 200


class LoginUserAPI(Resource):
    def post(self):
        """
        Authenticate user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            required: true
            description: User's login and password in JSON
            schema:
              $ref: '#/definitions/UserAuth'
        responses:
          200:
            description: Login successful
            schema:
              $ref: '#/definitions/UserData'
          401:
            description: Authentication failed
        """
        user = User.query.filter(and_(User.login == request.json['login'],
                                      User.password == request.json[
                                          'password'])).first()
        if user:
            return {'login': user.login, 'id': user.id}, 200
        return 'authentication failed', 401


class MessagesAPI(Resource):
    def get(self, sender_id, recipient_id):
        """
        List all messages between 2 users
        ---
        tags:
          - messages
        parameters:
          - in: path
            name: sender_id
            required: true
            description: Sender's id
            type: string
          - in: path
            name: recipient_id
            required: true
            description: Recipient's id
            type: string
        responses:
          200:
            description: List of messages
            schema:
              type: array
              items:
                type: object
                schema:
                  id: Message
                  properties:
                    id:
                      type: integer
                    sender_id:
                      type: integer
                    recipient_id:
                      type: integer
                    content:
                      type: string

        """
        messages = Message.query.filter(
            or_(and_(Message.recipient_id == recipient_id,
                     Message.sender_id == sender_id),
                and_(Message.recipient_id == sender_id,
                     Message.sender_id == recipient_id))).all()
        output = []
        for message in messages:
            output.append({'id': message.id,
                           'sender_id': message.sender_id,
                           'recipient_id': message.recipient_id,
                           'content': message.content})
        return output, 200

    def post(self, sender_id, recipient_id):
        """
        Send message to provided user
        ---
        tags:
          - messages
        parameters:
          - in: path
            name: sender_id
            required: true
            description: Sender's id
            type: string
          - in: path
            name: recipient_id
            required: true
            description: Recipient's id
            type: string
          - in: body
            name: body
            required: true
            description: JSON dictionary containing the message content
            schema:
              type: object
              properties:
                content:
                  type: string
        responses:
          201:
            description: Message has been sent
            schema:
              id: MessageId
              properties:
                message_id:
                  type: integer
        """
        message = Message(sender_id, recipient_id, request.json['content'])
        db_session.add(message)
        db_session.commit()
        return {'message_id': message.id}, 200


api.add_resource(UsersAPI, '/users')
api.add_resource(LoginUserAPI, '/login')
api.add_resource(OnlineUsersAPI, '/online')
api.add_resource(MessagesAPI, '/message/<sender_id>/<recipient_id>')

if __name__ == '__main__':
    app.run(debug=True)
