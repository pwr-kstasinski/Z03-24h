from uuid import uuid4
from flasgger import Swagger
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'Messengerify API',
    'uiversion': 3
}
swag = Swagger(app)

users = [
    {'uuid': '1a', 'login': 'awesome_user', 'password': 'awesome_password'},
    {'uuid': '2b', 'login': 'ugly_user', 'password': 'ugly_password'},
    {'uuid': '3c', 'login': 'fabulous_user', 'password': 'fabulous_password'},
]

messages = {
    ('1a', '3c'): [
        {'sender': '1a', 'content': 'Hi there!'},
        {'sender': '3c', 'content': 'Namaste!'},
    ]
}


class Users(Resource):
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
                uuid:
                  type: string
        """
        user = {
            'uuid': str(uuid4()),
            'login': request.json['login'],
            'password': request.json['password']
        }
        users.append(user)
        return {'login': user['login'], 'uuid': user['uuid']}, 201

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
        ext_users = []
        for user in users:
            ext_users.append({'login': user['login'], 'uuid': user['uuid']})
        return ext_users, 200


class LoginUser(Resource):
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

        for user in users:
            if user['login'] == request.json['login'] and user['password'] == request.json['password']:
                return {'login': user['login'], 'uuid': user['uuid']}
        return 'authentication failed', 401


class Message(Resource):
    def get(self, sender_uuid, recipient_uuid):
        """
        List all messages between 2 users
        ---
        tags:
          - messages
        parameters:
          - in: path
            name: sender_uuid
            required: true
            description: Sender's uuid
            type: string
          - in: path
            name: recipient_uuid
            required: true
            description: Recipient's uuid
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
                    sender:
                      type: string
                    content:
                      type: string

        """
        if (sender_uuid, recipient_uuid) in messages:
            return messages.pop((sender_uuid, recipient_uuid)), 200
        if (recipient_uuid, sender_uuid) in messages:
            return messages.pop((recipient_uuid, sender_uuid)), 200
        return [], 200

    def post(self, sender_uuid, recipient_uuid):
        """
        Send message to provided user
        ---
        tags:
          - messages
        parameters:
          - in: path
            name: sender_uuid
            required: true
            description: Sender's uuid
            type: string
          - in: path
            name: recipient_uuid
            required: true
            description: Recipient's uuid
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
          200:
            description: Message has been sent
        """
        if (sender_uuid, recipient_uuid) in messages:
            messages[(sender_uuid, recipient_uuid)].append({'sender': sender_uuid, 'content': request.json['content']})
            return 'message has been sent', 200
        if (recipient_uuid, sender_uuid) in messages:
            messages[(recipient_uuid, sender_uuid)].append({'sender': sender_uuid, 'content': request.json['content']})
            return 'message has been sent', 200
        messages[(sender_uuid, recipient_uuid)] = [{'sender': sender_uuid, 'content': request.json['content']}]
        return 'message has been sent', 200


api.add_resource(Users, '/users')
api.add_resource(LoginUser, '/login')
api.add_resource(Message, '/message/<sender_uuid>/<recipient_uuid>')


if __name__ == '__main__':
    app.run(debug=True)
