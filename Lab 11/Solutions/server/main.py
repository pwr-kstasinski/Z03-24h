from typing import List, Dict

import uvicorn
import json
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from pylint.checkers.typecheck import _
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.util import asyncio
from sqlalchemy_utils import database_exists

import crud
import database_models
import schemas
from database import SessionLocal, engine


database_models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()


class UserConnectionManager:
    def __init__(self):
        self.command_refreshUserList = 'refreshUserList'
        self.command_newMessage = 'newMessage'
        self.command_messageRead = 'messageRead'
        self.active_connections: dict[int, WebSocket] = {}  # userId, websocket

    async def connect(self, websocket: WebSocket, user_id: int):
        print(str(user_id) + " connected\n")
        await websocket.accept()
        await self.broadcast_refresh_user_list()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        print(str(user_id) + " disconnected\n")
        self.active_connections.pop(user_id, None)
        await self.broadcast_refresh_user_list()

    async def message_sent_to(self, sender_id: int, recipient_id: int):
        print(str(sender_id) + " sends to " + str(recipient_id))
        socket = self.active_connections.get(recipient_id, None)
        if socket is not None:
            print("Sending command to "+str(recipient_id)+"\n")
            jsonCommand = json.dumps({'command': self.command_newMessage, 'sender_id': sender_id})
            await socket.send_json(jsonCommand)

    async def broadcast_new_common_message(self):
        print("Broadcast new common message\n")
        for key in self.active_connections:
            jsonCommand = json.dumps({'command': self.command_messageRead, 'recipient_id': -1})
            await self.active_connections[key].send_json(jsonCommand)

    async def message_read(self, sender_id: int, recipient_id: int):
        print("Message from " + str(sender_id) + " read by " + str(recipient_id))
        socket = self.active_connections.get(sender_id, None)
        if socket is not None:
            print("Sending command to "+str(sender_id)+"\n")
            jsonCommand = json.dumps({'command': self.command_messageRead, 'recipient_id': recipient_id})
            await socket.send_json(jsonCommand)

    async def broadcast_refresh_user_list(self):
        print("Broadcast refresh user list\n")
        for key in self.active_connections:
            jsonCommand = json.dumps({'command': self.command_refreshUserList})
            await self.active_connections[key].send_json(jsonCommand)


websocketsManager = UserConnectionManager()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# resource token, JWT token, OIDC protocol (identity server - narzędzia: auth0, kcloack)

def get_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=int(token))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.websocket("/ws")
async def websocket_endpoint(
        websocket: WebSocket,
        current_user_id: int
):
    await websocketsManager.connect(websocket, current_user_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
    except WebSocketDisconnect:
        print("Websocket disconnected, user_id: " + str(current_user_id) + " ~~~~~~~~~~~~~~~~~~")
        await websocketsManager.disconnect(current_user_id)
        db = SessionLocal()
        crud.unmark_user_as_active(db, current_user_id)
        db.close()


@app.put("/inactive_user", status_code=200)
def mark_as_active(current_user: schemas.User = Depends(get_user_from_token),
                   db: Session = Depends(get_db)):
    current_user_id = current_user.id
    crud.mark_user_as_active(db, current_user_id)
    return


@app.put("/active_user", status_code=200)
def unmark_as_active(current_user: schemas.User = Depends(get_user_from_token),
                     db: Session = Depends(get_db)):
    current_user_id = current_user.id
    crud.unmark_user_as_active(db, current_user_id)
    return


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nickname(db, nick=user.nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")
    await websocketsManager.broadcast_refresh_user_list()
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/active_users/", response_model=List[schemas.UserActive])
def read_active_users(db: Session = Depends(get_db),
                      current_user: schemas.User = Depends(get_user_from_token)):
    users = crud.get_users_all(db=db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = crud.get_user_by_nickname(db, nick=form_data.username)
    if user_dict is None:
        raise HTTPException(status_code=400, detail="Incorrect username")
    password = user_dict.hashed_password
    if not password == form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"access_token": user_dict.id, "token_type": "bearer"}


@app.post("/messages/{messageTo}/", response_model=schemas.Message)
async def post_message(
        messageTo: str, message: schemas.MessageCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_user_from_token)
):
    current_user_id = current_user.id

    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    db_recipient = crud.get_user_by_nickname(db, nick=messageTo)
    if db_recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")

    result = crud.create_message(db=db, message=message, recipient_id=db_recipient.id, sender_id=current_user_id)
    await websocketsManager.message_sent_to(recipient_id=db_recipient.id, sender_id=current_user_id)
    return result


@app.post("/common_message", response_model=schemas.CommonMessage)
async def post_common_message(message: schemas.MessageCreate,
                              db: Session = Depends(get_db),
                              current_user: schemas.User = Depends(get_user_from_token)
                              ):
    current_user_id = current_user.id

    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    current_user = crud.get_user(db, current_user_id)
    current_user_nickname = current_user.nickname

    result = crud.create_common_message(db=db,
                                        message=message,
                                        sender_id=current_user_id,
                                        sender_nickname=current_user_nickname)

    await websocketsManager.broadcast_new_common_message()

    return result


@app.get("/messages/{messageFrom}", response_model=List[schemas.Message])
def get_messages(messageFrom: str,
                 db: Session = Depends(get_db),
                 current_user: schemas.User = Depends(get_user_from_token)):
    current_user_id = current_user.id

    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    db_sender = crud.get_user_by_nickname(db, nick=messageFrom)
    if db_sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")
    messages = crud.get_messages_by_users_id(db, sender_id=db_sender.id, recipient_id=current_user_id)
    return messages


@app.get("/common_messages", response_model=List[schemas.CommonMessage])
def get_common_messages(db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(get_user_from_token)):
    current_user_id = current_user.id
    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    messages = crud.get_common_messages(db)
    return messages


@app.get("/all_user_messages", response_model=List[schemas.Message])
def get_user_messages(
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_user_from_token)):
    current_user_id = current_user.id

    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    messages = crud.get_user_all_messages(db, user_id=current_user_id)
    return messages


@app.put("/mark_message_as_viewed", status_code=200)
async def mark_message_as_viewed(message_id: int,
                                 sender_id: int,
                                 db: Session = Depends(get_db),
                                 current_user: schemas.User = Depends(get_user_from_token)):
    crud.mark_message_as_viewed(db=db, message_id=message_id)
    await websocketsManager.message_read(sender_id=sender_id, recipient_id=current_user.id)
    return


@app.put("/mark_multiple_messages_as_viewed", status_code=200)
async def mark_multiple_messages_as_viewed(messages_ids: List[int],
                                           sender_id: int,
                                           db: Session = Depends(get_db),
                                           current_user: schemas.User = Depends(get_user_from_token)):
    crud.mark_multiple_messages_as_viewed(db=db, messages_ids=messages_ids)
    await websocketsManager.message_read(sender_id=sender_id, recipient_id=current_user.id)
    return


@app.get("/all_messages/", response_model=List[schemas.Message])
def getAllMessages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_messages(db, skip=skip, limit=limit)
    return items


@app.get("/conversation/", response_model=List[schemas.Message])
def get_conversation(otherUserNickName: str,
                     db: Session = Depends(get_db),
                     current_user: schemas.User = Depends(get_user_from_token)):
    current_user_id = current_user.id
    otherUser = crud.get_user_by_nickname(db, nick=otherUserNickName)
    if otherUser is None:
        raise HTTPException(status_code=404, detail="Other user not found")
    messages = crud.get_conversation(db=db, user_id=current_user_id, otherUser_id=otherUser.id)
    return messages


isHealthy = True


@app.get("/health_status/")
def check(response: Response):
    if isHealthy:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return


@app.post("/health_status/")
def change():
    global isHealthy
    isHealthy = False
    return "I'm sick now!"


"""
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
