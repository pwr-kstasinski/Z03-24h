from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



# __________________________________________________________________

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), unique=False, nullable=False)




@app.route('/sent-message/from-<send_user_id>/destination-<destination_user_id>', methods=['GET'])
def sendMessage(send_user_id, destination_user_id):
    return jsonify(message="text data from " + send_user_id + " to " + destination_user_id)


#@app.route('/users/new/<new_user_id>/<user_nickname>', methods=['POST'])
@app.route('/users/new', methods=['POST'])
def newUser():
  #   users = User.query.all()
  #
  #   output = ""
  #   # user = User.query.get_or_404(new_user_id)
  #
  #
    user = User(id=request.json["id"], nickname=request.json["nickname"])
  #  print("\n\n" + str(user.nickname) + "\n\n")
    db.session.add(user)
    db.session.commit()

    return jsonify(id=user.id, nickname=user.nickname)



@app.route('/users/login', methods=["POST"])
def logIn():
   # auth = request.authoriazation
    r = request.json['id']
    user = User.query.get_or_404(r)
  #  if not auth or not auth.nickname or not auth.id:
    return jsonify(id=user.id, nickname=user.nickname)




#@app.route('/send-message', methods=['GET'])
#def send


if __name__ == "__main__":
    app.run(debug=True)                 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
