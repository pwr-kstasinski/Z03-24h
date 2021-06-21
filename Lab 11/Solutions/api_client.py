import requests as req

api = 'http://localhost:5000/'


def send_message(sender, receiver, msg_content):
    url = api + 'Users/send_message'
    data = {
        "meta": {
            "method": "send_message",
            "args": {
                "sender": sender,
                "receiver": receiver,
                "msg_content": msg_content
            }
        }
    }

    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    return response


def get_messages_addressed_to(username):
    url = api + 'Messages/get_messages_addressed_to'
    params = {"receiver_name": username}
    response = req.get(url, params=params)
    return response


def combine_messages_into_chat(username):
    messages_json = get_messages_addressed_to(username).json()
    dict_messages = messages_json['meta']['result']['result']  # {'id':[], 'rec':[], 'send':[], 'cont':[]}
    chat_string = ''
    for (s, c) in zip(dict_messages['sen'], dict_messages['cont']):
        line = f'from: {s}: {c}\n'
        chat_string += line

    return chat_string


def get_conversation(username):   # username is receiver of the messages
    url = api + 'Messages/get_conversation'
    params = {"receiver_name": username}
    response = req.get(url, params=params)
    conversation_json = response.json()['meta']['result']['result']
    return conversation_json


def login(username, password):
    url = api + 'Users/login'
    data = {
        "meta": {
            "method": "login",
            "args": {
                "user_name": username,
                "user_password": password
            }
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    return response


def register(username, password):
    url = api + 'Users/register'
    data = {
        "meta": {
            "method": "register",
            "args": {
                "user_name": username,
                "user_password": password
            }
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    print(response.json())
    return response


def get_users():
    url = api + 'Users/'
    response = req.get(url)
    users_list = response.json()['data']
    return users_list


def mark_as_seen(id):
    url = api + 'Messages/'+str(id)
    data = {
        "data": {
            "attributes": {
                "read": True,
            },
            "type": "Message",
            "id": id
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.patch(url, json=data, headers=headers)
    return {'result': {'success': response}}


def set_status(id, status):
    url = api + 'Users/'+str(id)
    data = {
        "data": {
            "attributes": {
                "is_online": status
            },
            "type": "User",
            "id": id
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.patch(url, json=data, headers=headers)
    return {'result': {'success': response}}


def get_number_of_unread_messages(receiver_name, sender_name):   # username is receiver of the messages
    url = api + 'Messages/get_number_of_unread_messages'
    params = {"receiver_name": receiver_name, "sender_name": sender_name}
    response = req.get(url, params=params)
    number_of_unread_messages = response.json()['meta']['result']['result']

    return number_of_unread_messages