from tkinter import Tk, Frame, Label, Button, Entry, E, W, N, S, BOTH, StringVar, Text, DISABLED, INSERT, NORMAL, END, \
    Toplevel

import json
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
from openapi_client.model.message_create import MessageCreate
from openapi_client.model.user_create import UserCreate


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
    # Configure OAuth2 access token for authorization: OAuth2PasswordBearer
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    configuration.access_token = str(token)

    result = False
    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        message_to = receiverNickname
        message_create = MessageCreate(
            content=message
        )  # MessageCreate |

        try:
            api_response = api_instance.post_message_messages_message_to_post(message_to, message_create)
            pprint(api_response)
            result = True
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->post_message_messages_message_to_post: %s\n" % e)
        return result

def getActiveUsers(token:str):
    # Configure OAuth2 access token for authorization: OAuth2PasswordBearer
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
                result=api_response
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->read_active_users_active_users_get: %s\n" % e)
    return result

class ActiveUserList(Toplevel):
    def __init__(self, userlist):
        super().__init__()

        self.userlist = userlist
        self.frame = Frame(self)
        self.initUI()

    def initUI(self):
        self.frame.pack(fill=BOTH, expand=True)
        self.textList = Text(self.frame)
        self.textList.grid(row=0, column=0, columnspan=2, sticky=E + W + N + S)
        self.textList.config(state=NORMAL)
        for user in self.userlist:
            self.textList.insert(INSERT, "nickname: " + user['nickname'] + "; last active: " + user['last_active'].strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        self.textList.configure(state=DISABLED)


class Messenger(Toplevel):
    def __init__(self, token: str, username: str):
        super().__init__()
        self.token = token
        self.username = username
        self.frame = Frame(self)
        self.receiverNickname = None

        self.initUI()

    def refreshBtn(self):
        if self.receiverNickname is not None:
            receivedMessages = getMessages(self.token, self.receiverNickname)

            if receivedMessages is not None:
                for message in receivedMessages:
                    self.textTo.configure(state=NORMAL)
                    self.textTo.insert(INSERT, message['content'] + "\n")
                    self.textTo.configure(state=DISABLED)
        pass

    def sendBtn(self):
        if self.receiverNickname is not None:
            message = self.entryNewMessageFrom.get()

            result = sendMessage(self.token, self.receiverNickname, message)

            if result:
                self.textFrom.configure(state=NORMAL)
                self.textFrom.insert(INSERT, message + "\n")
                self.textFrom.configure(state=DISABLED)
        pass

    def resetUI(self):
        self.strToSet.set("Recipent nickname not set")
        self.receiverNickname = None

        self.textTo.configure(state=NORMAL)
        self.textTo.delete('1.0', END)
        self.textTo.configure(state=DISABLED)

        self.textFrom.configure(state=NORMAL)
        self.textFrom.delete('1.0', END)
        self.textFrom.configure(state=DISABLED)
        pass

    def confirmIDsBtn(self):
        self.resetUI()

        self.receiverNickname = self.entryTo.get()
        self.strToSet.set("Recipent nickname: {}".format(self.receiverNickname))
        pass

    def getActiveUsersBtn(self):

        userlist = getActiveUsers(self.token)

        if userlist:
            self.new = ActiveUserList(userlist)

        pass

    def initUI(self):
        self.strToSet = StringVar()
        self.strToSet.set("Recipent nickname not set")

        self.frame.pack(fill=BOTH, expand=True)
        row = 0

        self.buttonGetActiveUsers = Button(self.frame, text="Show active users", command=self.getActiveUsersBtn)
        self.buttonGetActiveUsers.grid(row=row, rowspan=4, column=0, columnspan=2, sticky=W + E + S + N)
        row = row + 1

        self.labelToInfo = Label(self.frame, text="Enter recipent nickname")
        self.labelToInfo.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.entryTo = Entry(self.frame)
        self.entryTo.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.buttonConfirmIDs = Button(self.frame, text="Confirm recipent nickname", command=self.confirmIDsBtn)
        self.buttonConfirmIDs.grid(row=row, column=2, columnspan=2, sticky=W + E + S + N)
        row = row + 1

        self.labelFromSet = Label(self.frame, text="Logged as {}".format(self.username))
        self.labelFromSet.grid(row=row, column=0, columnspan=2, sticky=E + W + N)

        self.labelToSet = Label(self.frame, textvariable=self.strToSet)
        self.labelToSet.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.textFrom = Text(self.frame)
        self.textFrom.grid(row=row, column=0, columnspan=2, sticky=E + W + N)
        self.textFrom.config(state=DISABLED)

        self.textTo = Text(self.frame)
        self.textTo.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        self.textTo.config(state=DISABLED)
        row = row + 1

        self.entryNewMessageFrom = Entry(self.frame)
        self.entryNewMessageFrom.grid(row=row, column=0, columnspan=2, sticky=E + W + N)

        self.buttonRefresh = Button(self.frame, text="Refresh", command=self.refreshBtn)
        self.buttonRefresh.grid(row=row, rowspan=2, column=2, columnspan=2, sticky=W + E + S + N)
        row = row + 1

        self.buttonSend = Button(self.frame, text="Send message", command=self.sendBtn)
        self.buttonSend.grid(row=row, column=0, columnspan=2, sticky=W + E + S + N)


class MainMenu(Frame):

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
            self.newWindow(Messenger, token=result["token"], username=username)
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


root = Tk()
app = MainMenu()
root.mainloop()
