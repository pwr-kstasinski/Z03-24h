from flask import Flask, request, session, redirect, url_for, Blueprint
from flask_restplus import Api, Resource, fields
import time
from datetime import timedelta

app = Flask(__name__)
api = Api(app, doc='/doc')
app.secret_key = "super_secret_key"
app.permanent_session_lifetime = timedelta(minutes=5)

# SWAGGER STUFF
app.config['SWAGGER_UI_JSONEDITOR'] = True
m_login = api.model(
    'User Login', {'name': fields.String("none")})
m_message = api.model(
    'Message', {'content': fields.String("none")})


# storege
rooms = {"1": {
    "users": {
        "Jack": {
            "messages": [{"content": "Hello There Jack", "time": time.time(), "from": "someone"}]
        },
        "John": {
            "messages": []
        }
    }
}}


@api.route('/login')
class Login(Resource):
    @api.expect(m_login)
    def post(self):
        session.permanent = True
        user = api.payload["name"]
        session["user"] = user
        return {"status": "succes", "username": user}


@app.route('/room/<int:room_id>')
class Room(Resource):
    def doStuff(room_id):
        if not "user" in session:
            return {"message": "You need to log in"}

        user_id = session["user"]
        room_id = str(room_id)
        if not (room_id in rooms):
            return {"message": "User or Room not found"}, 204

        if not user_id in rooms[room_id]["users"]:
            rooms[room_id]["users"][user_id] = {"messages": []}

    def get(self, room_id):
        doStuff(room_id)
        messages = rooms[room_id]["users"][user_id]["messages"]
        rooms[room_id]["users"][user_id]["messages"] = []
        return {"new_messages": messages}

    def post(self, room_id):
        doStuff(room_id)
        message = request.json["message"]
        if not message:
            return {"message": "No message content"}, 204  # kod do poprawy

        for user in rooms[room_id]["users"]:
            if not user == user_id:
                user_obj = rooms[room_id]["users"][user]
                user_obj["messages"].append(
                    {"content": message, "time": time.time(), "from": user_id})

        return {"message": "succes"}, 201


if __name__ == '__main__':
    print("YEE")
    app.run(debug=True)
