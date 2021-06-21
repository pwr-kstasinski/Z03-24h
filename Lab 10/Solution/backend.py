import asyncio
import json

import websockets
from sqlalchemy import and_, or_

from database import db_session, User, Message

connected = set()


async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            message = json.loads(message)

            # try to log in
            if message['action'] == 'try_login':
                user = User.query.filter(
                    and_(User.login == message['login'],
                         User.password == message['password']
                         )).first()
                if user:
                    user.active = 1
                    db_session.commit()
                    await websocket.send(json.dumps({
                        'action': 'confirm_login',
                        'login': user.login,
                        'id': user.id,
                    }))
                    websocket.user_id = user.id

                    # inform other users
                    users = []
                    for user in User.query.order_by(User.active.desc()).all():
                        users.append({'login': user.login, 'id': user.id,
                                      'active': user.active})
                    for conn in connected:
                        await conn.send(json.dumps({'action': 'list_users', 'users': users}))
                else:
                    await websocket.send(
                        json.dumps({'action': 'failed_login'}))

            # log out
            elif message['action'] == 'logout':
                user = User.query.filter(User.id == message['user_id']).first()
                user.active = 0
                db_session.commit()

                await websocket.send(f'logged out: {user.id}')

                # send new users message to all sockets
                users = []
                for user in User.query.order_by(User.active.desc()).all():
                    users.append({'login': user.login, 'id': user.id,
                                  'active': user.active})
                for conn in connected:
                    await conn.send(json.dumps({'action': 'list_users', 'users': users}))

            # try to register
            elif message['action'] == 'try_register':
                user = User(message['login'], message['password'])
                user.active = 1
                try:
                    db_session.add(user)
                    db_session.commit()
                    await websocket.send(json.dumps({
                        'action': 'confirm_register',
                        'login': user.login,
                        'id': user.id,
                    }))

                    # inform other users
                    users = []
                    for user in User.query.order_by(User.active.desc()).all():
                        users.append({'login': user.login, 'id': user.id,
                                      'active': user.active})
                    for conn in connected:
                        await conn.send(json.dumps(
                            {'action': 'list_users', 'users': users}))
                except Exception:
                    await websocket.send(
                        json.dumps({'action': 'failed_register'}))

            # get all users
            elif message['action'] == 'get_users':
                users = []
                for user in User.query.all():
                    users.append({'login': user.login, 'id': user.id, 'active': user.active})
                await websocket.send(
                    json.dumps({'action': 'list_users', 'users': users}))

            # get message
            elif message['action'] == 'get_messages':
                messages = Message.query.filter(
                        or_(and_(Message.recipient_id == message['recipient'],
                                 Message.sender_id == message['sender']),
                            and_(Message.recipient_id == message['sender'],
                                 Message.sender_id == message['recipient']))).all()
                output = []
                sid = 0
                rid = 0
                for message in messages:
                    output.append({
                        'id': message.id,
                        'sender_id': message.sender_id,
                        'recipient_id': message.recipient_id,
                        'content': message.content,
                        'read': message.read,
                        'sent': str(message.sent)
                    })
                    sid = message.sender_id
                    rid = message.recipient_id

            # get unread message
            elif message['action'] == 'get_unread_messages':
                messages = Message.query.filter(
                    and_(
                        or_(
                            and_(Message.recipient_id == message['recipient'], Message.sender_id == message['sender']),
                            and_(Message.recipient_id == message['sender'], Message.sender_id == message['recipient']),
                        ),
                        Message.read == 0
                    )
                ).all()
                output = []
                sid = 0
                rid = 0
                for message in messages:
                    output.append({
                        'id': message.id,
                        'sender_id': message.sender_id,
                        'recipient_id': message.recipient_id,
                        'content': message.content,
                        'read': message.read,
                        'sent': str(message.sent)
                    })
                    sid = message.sender_id
                    rid = message.recipient_id

                # invoke
                for conn in connected:
                    await conn.send(json.dumps({'action': 'list_messages', 'sender': sid, 'recipient': rid, 'messages': output}))

            # mark message as read
            elif message['action'] == 'mark_read':
                message = Message.query.filter(Message.id == message['message_id']).first()
                message.read = 1
                db_session.commit()

            # send message
            elif message['action'] == 'send_message':
                message = Message(message['sender'], message['recipient'],
                                  message['content'])
                db_session.add(message)
                db_session.commit()

                # invoke
                for conn in connected:
                    await conn.send(
                        json.dumps({'action': 'list_messages', 'sender': message.sender_id,
                            'recipient': message.recipient_id, 'messages': [{
                            'id': message.id,
                            'sender_id': message.sender_id,
                            'recipient_id': message.recipient_id,
                            'content': message.content,
                            'read': 1,
                            'sent': str(message.sent)
                        }]}))

    finally:
        # Unregister.
        connected.remove(websocket)


start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
