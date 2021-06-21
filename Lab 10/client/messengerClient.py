from tkinter import Tk, Frame, Label, Button, Entry, E, W, N, S, BOTH, StringVar, Text, DISABLED, INSERT, NORMAL, END, \
    Toplevel, LEFT, RIGHT, Canvas, ttk

import json
from functools import partial
from datetime import datetime
import openapi_client
from typing import List
from openapi_client.api import default_api
from openapi_client.model import message
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
import asyncio
import websockets
import ast

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
from openapi_client.model.message_create import MessageCreate
from openapi_client.model.user_create import UserCreate

root = Tk()


def attemptLogin(username: str, password: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)

        result = {"correct": False}
        try:
            api_response = api_instance.login_token_post(username, password)

            result["correct"] = True
            result["token"] = api_response["access_token"]
            pprint(api_response)

        except openapi_client.ApiException as e:
            dataReturned = json.loads(e.body)
            result["reason"] = dataReturned["detail"]
            print("Exception when calling DefaultApi->login_token_post: %s\n" % e)
        return result


def registerUser(username: str, password: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        user_create = UserCreate(
            nickname=username,
            password=password,
        )  # UserCreate |

        result = {"correct": False}
        try:
            api_response = api_instance.create_user_users_post(user_create)
            pprint(api_response)
            result["correct"] = True

        except openapi_client.ApiException as e:
            dataReturned = json.loads(e.body)
            result["reason"] = dataReturned["detail"]
            print("Exception when calling DefaultApi->create_user_users_post: %s\n" % e)
        return result


def getMessages(token: str, messagesFrom: str):
    messages = None
    configuration = openapi_client.Configuration(host="http://localhost:8000")
    configuration.access_token = str(token)

    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        message_from = messagesFrom
        try:
            api_response = api_instance.get_messages_messages_message_from_get(message_from)
            pprint(api_response)
            if api_response:
                messages = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_messages_messages_message_from_get: %s\n" % e)

    return messages


def sendMessage(token: str, receiverNickname: str, message: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    configuration.access_token = str(token)
    result = None
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        message_to = receiverNickname
        message_create = MessageCreate(
            content=message
        )  # MessageCreate |
        try:
            api_response = api_instance.post_message_messages_message_to_post(message_to, message_create)
            pprint(api_response)
            if api_response:
                result = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_message_messages_message_to_post: %s\n" % e)
        return result


def getActiveUsers(token: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    configuration.access_token = str(token)

    result = None
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        try:
            api_response = api_instance.read_active_users_active_users_get()
            pprint(api_response)
            if api_response:
                result = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->read_active_users_active_users_get: %s\n" % e)
    return result


def getUserMessages(token: str):
    configuration = openapi_client.Configuration(host="http://localhost:8000")
    configuration.access_token = str(token)
    result = None
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        try:
            api_response = api_instance.get_user_messages_all_user_messages_get()
            pprint(api_response)
            if api_response:
                result = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_user_messages_all_user_messages_get: %s\n" % e)
    return result


def getConversation(token: str, otherUserName):
    configuration = openapi_client.Configuration(host="http://localhost:8000")
    configuration.access_token = str(token)
    result = None
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        other_user_nick_name = otherUserName
        try:
            api_response = api_instance.get_conversation_conversation_get(other_user_nick_name)
            pprint(api_response)
            if api_response:
                result = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_conversation_conversation_get: %s\n" % e)
    return result


def markMultipleMessagesAsViewed(token: str, sender_id: int, messagesId: List[int]):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    configuration.access_token = str(token)
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        request_body = messagesId
        try:
            api_response = api_instance.mark_multiple_messages_as_viewed_mark_multiple_messages_as_viewed_put(sender_id,
                                                                                                              request_body)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print(
                "Exception when calling DefaultApi->mark_multiple_messages_as_viewed_mark_multiple_messages_as_viewed_put: %s\n" % e)


def markUserAsActive(token: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    configuration.access_token = str(token)
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        try:
            api_response = api_instance.mark_as_active_inactive_user_put()
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->mark_as_active_inactive_user_put: %s\n" % e)


def getCommonMessages(token: str):
    configuration = openapi_client.Configuration(host="http://localhost:8000")
    configuration.access_token = str(token)
    result = None
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        try:
            # Get Common Messages
            api_response = api_instance.get_common_messages_common_messages_get()
            pprint(api_response)
            if api_response:
                result = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_common_messages_common_messages_get: %s\n" % e)
    return result


def sendCommonMessage(token: str, message: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    configuration.access_token = str(token)
    result = None
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        message_create = MessageCreate(
            content=message
        )  # MessageCreate |
        try:
            api_response = api_instance.post_common_message_common_message_post(message_create)
            pprint(api_response)
            if api_response:
                result = api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_message_messages_message_to_post: %s\n" % e)
        return result


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class User:
    def __init__(self, id: int, nickname: str, active: bool, lastMessage: datetime = datetime.min,
                 unreadMessages: int = 0):
        self.id = id
        self.nickname = nickname
        self.lastMessage = lastMessage
        self.unreadMessages = unreadMessages
        self.active = int(active)


async def getUsersAndMessages(token: str):
    allUserList = await getActiveUsers(token)
    userMessageList = await getUserMessages(token)

    return allUserList, userMessageList


class UserListWindow(Toplevel):
    def __init__(self, token, nickname):
        super().__init__()

        # self.hello()
        self.nickname = nickname
        self.token = token

        self.baseFrame = Frame(self)
        self.listFrame = Frame(self.baseFrame, highlightbackground="black", highlightthickness=1)
        self.conversationFrame = Frame(self.baseFrame, highlightbackground="black", highlightthickness=1)

        self.baseFrame.pack(fill=BOTH, expand=True)
        self.listFrame.pack(fill=BOTH, expand=True, side=LEFT)
        self.conversationFrame.pack(fill=BOTH, expand=True, side=RIGHT)

        self.row = 0
        self.receiverNickname = None
        self.receiverId = None
        self.entryNewMessage = None
        self.messages = None

        markUserAsActive(self.token)

        self.updateUserList()

        loop = asyncio.get_event_loop()
        self.tasks = []
        self.tasks.append(loop.create_task(self.hello()))
        self.tasks.append(loop.create_task(self.updater()))
        loop.run_forever()

    async def hello(self):
        uri = "ws://localhost:8000/ws?current_user_id=" + str(self.token)
        async with websockets.connect(uri) as websocket:
            while True:
                greeting = await websocket.recv()
                jsonDict = ast.literal_eval(json.loads(greeting))
                print(str(jsonDict) + "~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Executing command " + jsonDict['command'] + "~~~~~~~~~~~~~~~~~~~~~~~~~~")
                if jsonDict['command'] == 'refreshUserList':
                    self.updateUserList()
                elif jsonDict['command'] == 'newMessage':
                    if jsonDict['sender_id'] == self.receiverId:
                        self.refreshChat()
                    else:
                        self.updateUserList()
                elif jsonDict['command'] == 'messageRead':
                    if jsonDict['recipient_id'] == self.receiverId:
                        self.refreshChat()
        pass

    async def updater(self):
        while True:
            root.update()
            await asyncio.sleep(1 / 120)

    def updateUserList(self):
        allUserList = getActiveUsers(self.token)
        userMessageList = getUserMessages(self.token)
        userList = self.createUserList(allUserList, userMessageList)
        self.initUI(userList)

    def createUserList(self, allUserList, userMessageList):
        localUserDict = {}

        for userDict in allUserList:
            localUserDict[userDict['id']] = (
                User(id=userDict['id'], nickname=userDict['nickname'], active=userDict['active']))

        if userMessageList is not None:
            for messDict in userMessageList:
                otherUserId = messDict['sender_id'] if self.token == messDict['recipient_id'] else messDict[
                    'recipient_id']
                if messDict['send_time'] > localUserDict[otherUserId].lastMessage:
                    localUserDict[otherUserId].lastMessage = messDict['send_time']
                if messDict['recipient_id'] == self.token and not messDict['viewed']:
                    localUserDict[otherUserId].unreadMessages = localUserDict[otherUserId].unreadMessages + 1

        userList = []
        for key in localUserDict:
            userList.append(localUserDict[key])

        userList.sort(key=lambda x: (x.lastMessage, x.active))
        userList.reverse()

        return userList

    def sendBtn(self):
        if self.receiverNickname is not None:
            message = self.entryNewMessage.get()
            if self.receiverId == -1:
                result = sendCommonMessage(self.token, message)
            else:
                result = sendMessage(self.token, self.receiverNickname, message)
            if result is not None:
                self.addMessage(result)
        return

    def addMessage(self, message):
        color = "sky blue" if message['sender_id'] == self.token else 'pale green'
        messageFrame = Frame(self.messagesFrame.scrollable_frame, highlightbackground="black", highlightthickness=1)
        messageFrame.config(background=color)
        messageFrame.grid(row=self.row, column=1 if message['sender_id'] == self.token else 0)
        sendTimeLabel = Label(messageFrame, text="{}".format(message['send_time'].strftime("%m/%d/%Y, %H:%M:%S")))
        sendTimeLabel.grid(row=0, column=0, sticky=E + W + N + S)
        sendTimeLabel.config(bg=color)
        nameLabel = Label(messageFrame, text="{}".format(str(message['sender_nickname']) + " writes:" if self.receiverId == -1 else (
                                                         self.nickname if message['sender_id'] == self.token else
                                                         self.receiverNickname) +
                                             ' writes (' + ('viewed' if message['viewed'] else 'not viewed') + '):'))
        nameLabel.grid(row=1, column=0, sticky=E + W + N + S)
        nameLabel.config(bg=color)
        contentLabel = Label(messageFrame, text=message['content'], wraplength=200)
        contentLabel.grid(row=2, column=0, sticky=E + W + N + S)
        contentLabel.config(bg=color)
        self.row = self.row + 1
        self.messagesFrame.canvas.update_idletasks()
        self.messagesFrame.canvas.yview_moveto(1.0)

    def populateMessagesFrame(self, messages):
        self.row = 0
        messagesToMarkAsViewed = []
        if messages is not None:
            for mess in messages:
                if 'recipient_id' in mess:
                    if self.token == mess['recipient_id'] and not mess['viewed']:
                        messagesToMarkAsViewed.append(mess['id'])
                        mess['viewed'] = True
                self.addMessage(mess)
            if messagesToMarkAsViewed:
                markMultipleMessagesAsViewed(self.token, self.receiverId, messagesToMarkAsViewed)
        return

    def refreshChat(self):
        if self.receiverId == -1:
            messages = getCommonMessages(self.token)
        else:
            messages = getConversation(self.token, self.receiverNickname)
        for widgets in self.conversationFrame.winfo_children():
            widgets.destroy()
        infoLabel = Label(self.conversationFrame, text="Chat with {}".format(
            self.receiverNickname if self.receiverId != -1 else "all"))
        infoLabel.grid(row=0, column=0, sticky=E + W + N + S)

        self.messagesFrame = ScrollableFrame(self.conversationFrame)
        self.messagesFrame.scrollable_frame.columnconfigure(0, weight=1)
        self.messagesFrame.scrollable_frame.columnconfigure(1, weight=1)
        Label(self.messagesFrame.scrollable_frame, width=20).grid(row=0, column=0, sticky=E + S)
        Label(self.messagesFrame.scrollable_frame, width=20).grid(row=0, column=1, sticky=E + S)

        self.populateMessagesFrame(messages)
        self.messagesFrame.grid(row=1, rowspan=6, column=0, sticky=E + W + N + S)

        self.entryNewMessage = Entry(self.conversationFrame)
        self.entryNewMessage.grid(row=7, column=0, sticky=E + W + N + S)

        self.buttonSend = Button(self.conversationFrame, text="Send message", command=self.sendBtn)
        self.buttonSend.grid(row=8, column=0, sticky=E + W + N + S)
        return

    def openChat(self, otherUserName: str, otherUser_id: int):
        self.receiverId = otherUser_id
        self.receiverNickname = otherUserName
        self.refreshChat()
        return

    def initUI(self, userList):

        row = 0
        for widgets in self.listFrame.winfo_children():
            widgets.destroy()

        self.infoLabel = Label(self.listFrame, text="Logged as {}".format(self.nickname))
        self.infoLabel.grid(row=row, column=0, columnspan=3, sticky=E + W + N)
        row = row + 1

        self.buttonLabel = Label(self.listFrame, text="Open chat with")
        self.buttonLabel.grid(row=row, column=0, sticky=E + W + N)

        self.ureadLabel = Label(self.listFrame, text="Unread messages")
        self.ureadLabel.grid(row=row, column=1, sticky=E + W + N)

        self.activeLabel = Label(self.listFrame, text="Is active")
        self.activeLabel.grid(row=row, column=2, sticky=E + W + N)
        row = row + 1

        self.UIList = []

        for user in userList:
            button = Button(self.listFrame, text=user.nickname, command=partial(self.openChat, user.nickname, user.id))
            button.grid(row=row, column=0, sticky=E + W + N)
            unreadMessages = Label(self.listFrame, text=str(user.unreadMessages))
            unreadMessages.grid(row=row, column=1, sticky=E + W + N)
            active = Label(self.listFrame, text='Active' if user.active else 'Inactive')
            active.grid(row=row, column=2, sticky=E + W + N)
            rowTuple = button, unreadMessages, active
            self.UIList.append(rowTuple)
            row = row + 1

        self.commonChatButton = Button(self.listFrame, text="Open commmon chat", command=partial(self.openChat, '', -1))
        self.commonChatButton.grid(row=row, column=0, columnspan=3, sticky=E + W + N + S)


class LoginRegisterWindow(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def newWindow(self, _class, token, username):
        self.new = _class(token, username)

    def loginBtn(self):

        username = self.entryLogin.get()
        password = self.entryPassword.get()

        result = attemptLogin(username, password)
        if result["correct"]:
            self.strInfo.set("Logged in")
            self.newWindow(UserListWindow, token=result["token"], username=username)
            # messenger = Messenger(token=result["token"])
        else:
            self.strInfo.set(result["reason"])

    def registerBtn(self):
        username = self.entryLogin.get()
        password = self.entryPassword.get()

        result = registerUser(username, password)
        if result["correct"]:
            self.strInfo.set("User registered")
            pass
        else:
            self.strInfo.set(result["reason"])
        pass

    def initUI(self):
        self.strInfo = StringVar()

        self.strInfo.set("")

        self.pack(fill=BOTH, expand=True)
        row = 0

        self.labelLogin = Label(self, text="Username: ")
        self.labelLogin.grid(row=row, column=0, sticky=E + W + N)

        self.entryLogin = Entry(self)
        self.entryLogin.grid(row=row, column=1, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.labelPassword = Label(self, text="Password: ")
        self.labelPassword.grid(row=row, column=0, sticky=E + W + N)

        self.entryPassword = Entry(self)
        self.entryPassword.grid(row=row, column=1, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.buttonLogin = Button(self, text="Login", command=self.loginBtn)
        self.buttonLogin.grid(row=row, column=0, columnspan=3, sticky=W + E + S + N)
        row = row + 1

        self.buttonRegister = Button(self, text="Register", command=self.registerBtn)
        self.buttonRegister.grid(row=row, column=0, columnspan=3, sticky=W + E + S + N)
        row = row + 1

        self.labelInfo = Label(self, textvariable=self.strInfo)
        self.labelInfo.grid(row=row, column=0, columnspan=3, sticky=E + W + N)


app = LoginRegisterWindow()
root.mainloop()
