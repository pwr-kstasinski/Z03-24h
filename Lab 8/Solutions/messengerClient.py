import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
from tkinter import Tk, Frame, Label, Button, Entry, E, W, N, S, BOTH, StringVar, Text, DISABLED, INSERT, NORMAL, END


# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.

def getMessages(sendTo, sendFrom):
    messages = None
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        message_to = sendTo  # int |
        message_from = sendFrom  # int |
        username = "{}".format(sendTo)  # str |
        password = "1"  # str |

        try:
            # Getmessages
            api_response = api_instance.get_messages_messages_put(message_to, message_from, username, password)
            pprint(api_response)
            if not api_response['empty']:
                messages = api_response['messages']
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_messages_messages_put: %s\n" % e)

    return messages


def sendMessage(sendTo: int, sendFrom: int, message: str):
    configuration = openapi_client.Configuration(
        host="http://localhost:8000"
    )
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        message_to = sendTo  # int |
        message_from = sendFrom  # int |
        username = "{}".format(sendFrom)  # str |
        password = "1"  # str |

        try:
            # Sendmessage
            api_response = api_instance.send_message_messages_post(message_to, message_from, message, username,
                                                                   password)
            pprint(api_response)
            return True
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->send_message_messages_post: %s\n" % e)

    return False


class GUI(Frame):

    def __init__(self):
        super().__init__()

        self.senderID = None
        self.receiverID = None

        self.initUI()

    def refreshBtn(self):
        if not (self.senderID is None or self.receiverID is None):
            receivedMessages = getMessages(self.senderID, self.receiverID)

            if receivedMessages is not None:
                for message in receivedMessages:
                    self.textTo.configure(state=NORMAL)
                    self.textTo.insert(INSERT, message + "\n")
                    self.textTo.configure(state=DISABLED)
        pass

    def sendBtn(self):
        if not (self.senderID is None or self.receiverID is None):
            message = self.entryNewMessageFrom.get()

            result = sendMessage(self.receiverID, self.senderID, message)

            if result:
                self.textFrom.configure(state=NORMAL)
                self.textFrom.insert(INSERT, message + "\n")
                self.textFrom.configure(state=DISABLED)
        pass

    def resetUI(self):
        self.strToSet.set("Recipent ID not set")
        self.strFromSet.set("Your ID not set")
        self.senderID = None
        self.receiverID = None

        self.textTo.configure(state=NORMAL)
        self.textTo.delete('1.0', END)
        self.textTo.configure(state=DISABLED)

        self.textFrom.configure(state=NORMAL)
        self.textFrom.delete('1.0', END)
        self.textFrom.configure(state=DISABLED)
        pass

    def confirmIDsBtn(self):
        self.resetUI()

        if self.entryFrom.get().isnumeric() and self.entryTo.get().isnumeric():
            self.senderID = int(self.entryFrom.get())
            self.receiverID = int(self.entryTo.get())

            self.strFromSet.set("Your ID: {}".format(self.senderID))
            self.strToSet.set("Recipent ID: {}".format(self.receiverID))
        pass

    def initUI(self):
        self.strToSet = StringVar()
        self.strFromSet = StringVar()

        self.strToSet.set("Recipent ID not set")
        self.strFromSet.set("Your ID not set")

        self.pack(fill=BOTH, expand=True)
        row = 0

        self.labelFromInfo = Label(self, text="Enter your ID")
        self.labelFromInfo.grid(row=row, column=0, columnspan=2, sticky=E + W + N)

        self.labelToInfo = Label(self, text="Enter recipent ID")
        self.labelToInfo.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.entryFrom = Entry(self)
        self.entryFrom.grid(row=row, column=0, columnspan=2, sticky=E + W + N)

        self.entryTo = Entry(self)
        self.entryTo.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.buttonConfirmIDs = Button(self, text="Confirm IDs", command=self.confirmIDsBtn)
        self.buttonConfirmIDs.grid(row=row, column=0, columnspan=4, sticky=W + E + S + N)
        row = row + 1

        self.labelFromSet = Label(self, textvariable=self.strFromSet)
        self.labelFromSet.grid(row=row, column=0, columnspan=2, sticky=E + W + N)

        self.labelToSet = Label(self, textvariable=self.strToSet)
        self.labelToSet.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        row = row + 1

        self.textFrom = Text(self)
        self.textFrom.grid(row=row, column=0, columnspan=2, sticky=E + W + N)
        self.textFrom.config(state=DISABLED)
        self.textFrom
        self.textTo = Text(self)
        self.textTo.grid(row=row, column=2, columnspan=2, sticky=E + W + N)
        self.textTo.config(state=DISABLED)

        row = row + 1

        self.entryNewMessageFrom = Entry(self)
        self.entryNewMessageFrom.grid(row=row, column=0, columnspan=2, sticky=E + W + N)

        self.buttonRefresh = Button(self, text="Refresh", command=self.refreshBtn)
        self.buttonRefresh.grid(row=row, rowspan=2, column=2, columnspan=2, sticky=W + E + S + N)
        row = row + 1

        self.buttonSend = Button(self, text="Send message", command=self.sendBtn)
        self.buttonSend.grid(row=row, column=0, columnspan=2, sticky=W + E + S + N)


root = Tk()
app = GUI()
root.mainloop()
