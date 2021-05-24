from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
import psycopg2
#import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'                      # haslo                      baza
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:programowanko2021@localhost/komunikator'
db = SQLAlchemy(app)


# __________________________________________________________________

class User(db.Model):
    __tablename__ = 'users'
    login = db.Column(db.String(25), primary_key=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    is_logged_in = db.Column(db.Boolean)

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    message_data = db.Column(db.String(), nullable=False)
    from_login = db.Column(db.String(25), nullable=False)
    destination_login = db.Column(db.String(25))

@app.route('/message/send', methods=['POST'])
def sendMessage():
    message = Message(message_data=request.json['message_data'], from_login=request.json['from_login'],
                      destination_login=request.json['destination_login'])
    db.session.add(message)
    db.session.commit()
    return jsonify(id=message.id, from_login=message.from_login, destination_login=message.destination_login)



@app.route('/message/get', methods=['POST'])
def getMessage():
    messages = db.session.query(Message).filter( (Message.destination_login.in_([str(request.json['login']), '']))
                                                 |
                                                 (Message.from_login == str(request.json['login'])))# and
                                            #    Message.message_id > request.json['id']).all()
    return_messages = []            # niewlasciwy nawias??
    for message in messages:
        if message.message_id >= int(request.json['id']):
            return_messages.append({"message_id": message.message_id, "from_login": message.from_login, "message": message.message_data, "destination_login": message.destination_login})

        # wiadomosci dla danego loginu i do wszystkich, od danego id(nie pobiera wszystkich wiadomosci za kazdym razem)
    return jsonify(return_messages)



@app.route('/users/new', methods=['POST'])
def newUser():
    user = User(login=request.json["login"], password=request.json["password"], is_logged_in=False)
  #  print("\n\n" + str(user.nickname) + "\n\n")
    db.session.add(user)
    db.session.commit()

    return jsonify(login=user.login)


@app.route('/users/login', methods=["POST"])
def logIn():            # troche niezgrabne, popraw kiedys, teraz malo czasu
    users = User.query.all()
    for user in users:
        if user.login == request.json['login'] and user.password == request.json['password']:
            db.session.query(User).filter(User.login == request.json['login']).first().is_logged_in = True
            db.session.commit()
            return jsonify(login=user.login)
#    r = request.json['login']
   # user = User.query.get_or_404(r)
    User.query.get_or_404()         # 404 nie ma w bazie
  #  if not auth or not auth.nickname or not auth.id:
    return jsonify(login=user.login)


@app.route('/users/logout', methods=["PUT"])
def logOut():
    db.session.query(User).filter(User.login == request.json['login']).first().is_logged_in = False
    db.session.commit()


# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NA FALSE ZMIENIA!!!!!!!!!!!!!!!!!
# @app.route('/users/update-login-status', methods=["PUT"])
# def updateLoginStatus():
#     db.session.query(User).filter(User.login == request.json['login']).first().is_logged_in = False
#     db.session.commit()


@app.route('/users/loggedin', methods=["GET"])
def loggedInUsers():
    logged_in_users = []
    users = User.query.all()
    for user in users:
        if user.is_logged_in:
            logged_in_users.append(user.login)

    return jsonify(logged_in_users=logged_in_users)






if __name__ == "__main__":
    app.run(debug=True)                 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
