from fastapi import FastAPI
import time
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.put('/join/{room_id}/{user_name}')
def join(room_id: str, user_name: str):
    if not room_id in rooms:
        return {"status": "fail", "couse": "No such room"}, 401
    if user_name in rooms[room_id]["users"]:
        return {"status": "succes", "message": f"Welcome back {user_name}"}, 200
    else:
        rooms[room_id]["users"][user_name] = {"messages": []}
        return {"status": "succes", "message": f"Welcome new user {user_name}"}, 201


@app.get('/room/{room_id}/{user_name}')
def getMessages(room_id: str, user_name: str):
    if not room_id in rooms:
        return {"status": "fail", "couse": "No such room"}, 401
    if not user_name in rooms[room_id]["users"]:
        return {"status": "fail", "couse": "No such user"}, 401

    new_messages = rooms[room_id]["users"][user_name]["messages"]
    rooms[room_id]["users"][user_name]["messages"] = []

    return {"messages": new_messages}, 200


@app.put('/room/{room_id}')
def createRoom(room_id: str):
    if room_id in rooms:
        return {"status": "fail", "couse": "Room with this name already exist"}, 401
    rooms[room_id] = {"users": {}}
    return {"status": "succes", "message": f"Created room {room_id}"}, 201


class Mesage(BaseModel):
    sender: str
    message: str


@app.post('/room/{room_id}')
def sendMsg(request: Mesage, room_id: str):
    if not room_id in rooms:
        return {"status": "fail", "couse": "No such room"}, 401
    if not request.sender in rooms[room_id]["users"]:
        return {"status": "fail", "couse": "No such user"}, 401

    room = rooms[room_id]["users"]
    for user in room:
        if not user == request.sender:
            msg = {
                "content": request.message,
                "time": time.time(),
                "from": request.sender
            }
            room[user]["messages"].append(msg)

    return {"status": "succes"}, 201
