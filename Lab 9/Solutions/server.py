from flask import Flask
from flask.helpers import send_from_directory
from flask_restplus import Api, Resource, reqparse, abort, fields, marshal_with
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app, version="2.0", title="Chatroom")
#Database
db = SQLAlchemy(app)

class UserModel(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    isLogged = db.Column(db.String, nullable=False)

class MessageModel(db.Model):

    idM = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)


db.create_all()

users_resource_fields ={
    'username': fields.String,
    'password': fields.String,
    'isLogged': fields.String
}

message_resource_fields = {
    'idM': fields.Integer,
    'source': fields.String,
    'destination': fields.String,
    'text': fields.String 
}

userCounter = 0
msgCounter = 0


users_args = reqparse.RequestParser()
users_args.add_argument("username", type=str)
users_args.add_argument("password", type=str)
users_args.add_argument("isLogged", type=str)

msg_args = reqparse.RequestParser()
msg_args.add_argument("source", type=str)
msg_args.add_argument("destination", type=str)
msg_args.add_argument("text", type=str)

msg_get_args = reqparse.RequestParser()
msg_get_args.add_argument("username", type=str, required=True)

@api.route('/login', endpoint='Login')
class Login(Resource):
    #login
    def put(self):
        args = users_args.parse_args()
        query = db.session.query(UserModel).filter_by(username=args["username"]).first()
        if query is not None:
            if query.password == args["password"]:
                query.isLogged = args["isLogged"]
                db.session.commit()
                return '', 200
            return {"error": "Wrong password"}, 400
        return {"error": "No such user"}, 400
    #add user
    def post(self):
        args = users_args.parse_args()
        print(args["username"])
        if (db.session.query(UserModel).filter_by(username=args["username"]).first() is not None)|(args["username"]=="@all"):
            return {'error': "User aleardy exists!"}, 400
        else:
            newUser = UserModel(username=args["username"], password=args["password"], isLogged="No")
            db.session.add(newUser)
            db.session.commit()
            return '', 200
    #Get online users
    def get(self):
        query = db.session.query(UserModel).filter_by(isLogged ='Yes').all()
        online = {}
        for users in query:
            online[users.username] = users.isLogged
        return {'onlineUsers' : online}, 200


api_post_msg_model = api.model('MessagePost', {'source' : fields.String, 'destination': fields.String, 'text': fields.String})
api_get_msg_model = api.model('MessageGet', {'username' : fields.String})
class Message(Resource):
    #send msgs
    @marshal_with(message_resource_fields)
    @api.expect(api_post_msg_model)
    def post(self):
        global msgCounter
        args = msg_args.parse_args()
        if args["destination"]=="@all":
            query = db.session.query(UserModel).filter_by(isLogged ='Yes').all()
            for user in query:
                if user.username != args["source"]:
                    msgCounter += 1
                    message = MessageModel(idM = msgCounter, source=args['source'], destination=user.username, text="@all " + args['text'])
                    db.session.add(message)
                    db.session.commit()
            return '', 200
        elif (db.session.query(UserModel).filter_by(username=args["destination"]).first() is not None):
            msgCounter += 1
            message = MessageModel(idM = msgCounter, source=args['source'], destination=args['destination'], text=args['text'])
            db.session.add(message)
            db.session.commit()
            return {'msgId': msgCounter}, 200
        else:
            return '', 400
    #recive msgs
    @marshal_with(message_resource_fields)
    @api.expect(api_get_msg_model)
    def put(self):
        args = msg_get_args.parse_args()
        myMsgs = db.session.query(MessageModel).filter_by(destination=args['username']).all()
        db.session.query(MessageModel).filter_by(destination=args['username']).delete()
        db.session.commit()
        print(myMsgs)
        if myMsgs:
            return myMsgs, 200
        else:
            return '', 400



api.add_resource(Message, "/msg")
api.add_resource(Login, "/login")




if __name__ == '__main__':
    app.run(debug=True)