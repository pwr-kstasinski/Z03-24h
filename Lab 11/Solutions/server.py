from flask import Flask
from flask.helpers import make_response
from flask_restplus import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.declarative.api import declarative_base
import os


app = Flask(__name__)
api = Api(app, version="2.0", title="Chatroom")

##########
#Database#
##########
#mariadbconnector
engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@{}:{}".format(os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'], os.environ['DB_PORT']))
engine.execute(r"CREATE DATABASE IF NOT EXISTS chatroomdb")
engine.execute(r"USE chatroomdb")

Base = declarative_base()
#db = SQLAlchemy(app)

class UserModel(Base):
    __tablename__ = "UserModel"
    username = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    isLogged = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

class MessageModel(Base):
    __tablename__ = "MessageModel"
    idM = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    source = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    destination = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(1000), nullable=False)


Base.metadata.create_all(bind=engine)


#session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

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
        query = session.query(UserModel).filter_by(username=args["username"]).first()
        if query is not None:
            if query.password == args["password"]:
                query.isLogged = args["isLogged"]
                session.commit()
                return '', 200
            return {"error": "Wrong password"}, 400
        return {"error": "No such user"}, 400
    #add user
    def post(self):
        args = users_args.parse_args()
        print(args["username"])
        if (session.query(UserModel).filter_by(username=args["username"]).first() is not None)|(args["username"]=="@all"):
            return {'error': "User aleardy exists!"}, 400
        else:
            newUser = UserModel(username=args["username"], password=args["password"], isLogged="No")
            session.add(newUser)
            session.commit()
            return '', 200
    #Get online users
    def get(self):
        query = session.query(UserModel).filter_by(isLogged ='Yes').all()
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
            query = session.query(UserModel).filter_by(isLogged ='Yes').all()
            for user in query:
                if user.username != args["source"]:
                    msgCounter += 1
                    message = MessageModel(idM = msgCounter, source=args['source'], destination=user.username, text="@all " + args['text'])
                    session.add(message)
                    session.commit()
            return '', 200
        elif (session.query(UserModel).filter_by(username=args["destination"]).first() is not None):
            msgCounter += 1
            message = MessageModel(source=args['source'], destination=args['destination'], text=args['text'])
            session.add(message)
            session.commit()
            return {'msgId': msgCounter}, 200
        else:
            return '', 400
    #recive msgs
    @marshal_with(message_resource_fields)
    @api.expect(api_get_msg_model)
    def put(self):
        args = msg_get_args.parse_args()
        myMsgs = session.query(MessageModel).filter_by(destination=args['username']).all()
        session.query(MessageModel).filter_by(destination=args['username']).delete()
        session.commit()
        print(myMsgs)
        if myMsgs:
            return myMsgs, 200
        else:
            return '', 400

isHealthy = True
@api.route('/health', endpoint='Health')
class Health(Resource):
    def get(self):
        global isHealthy
        res = make_response()
        if(isHealthy):
            res = make_response("succes", 200)
            res.status_code = 200
        else:
            res = make_response("fail", 500)
            res.status_code = 500
        return res

    def put(self):
        global isHealthy
        isHealthy = False
        return '', 200

api.add_resource(Message, "/msg")
api.add_resource(Login, "/login")
api.add_resource(Health, "/health")



if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')