import tkinter as tk
from tkinter import Entry, Label, Button, Frame
import requests as req

api = 'http://localhost:5000/'


class Window:
    root = tk.Tk()
    #root.geometry("200x400")
    client_name = ""
    entry_login_label = None
    entry_login_frame = None

    def __init__(self):
        self.root.title('Chat')
        self.entry_login_frame = Frame(self.root)
        self.entry_login_frame.grid(row=0)
        login_label = Label(self.entry_login_frame, text='Enter your nickname: ', font=('Arial', 12))
        self.entry_login_label = Entry(self.entry_login_frame, width=20, font=('Arial', 12))
        enter_chat_button = Button(self.entry_login_frame, text='Enter chat', font=('Arial', 12), command=lambda: self.enter_chat_button_on_click())

        login_label.grid(row=0, column=0)
        self.entry_login_label.grid(row=1, column=0)
        enter_chat_button.grid(row=2, column=0)
        self.root.mainloop()

    def enter_chat_button_on_click(self, is_logged = False, chat_label=None):
        if not is_logged:
            self.client_name = self.entry_login_label.get()
        else:
             chat_label.destroy()
        login_or_register(self.client_name)
        self.create_chat_window()

    def create_chat_window(self):
        self.entry_login_frame.destroy()
        nickname_label = Label(self.root, text='Your nickname: '+self.client_name, font=('Arial', 12))
        nickname_label.grid(row=0, column=0)
        chat_label = Label(self.root, text='', background='white', font=('Arial', 12))
        list_of_messages = get_messages_addressed_to(self.client_name).json()['meta']['result']['result']

        chat_window = ''
        for i in list_of_messages:
            chat_window += '\n'+i['sender']+": "+i['content']

        chat_label.configure(text=chat_window)
        chat_label.grid(row=1, column=0)

        message_field = Entry(self.root, background='white', width=20, font=('Arial', 12))
        message_field.grid(row=2, column=0)
        receiver_field = Entry(self.root, background='white', width=20, font=('Arial', 12))
        receiver_field.grid(row=3, column=0)
        send_button = Button(self.root, text='send', font=('Arial', 12), command=lambda: self.send(receiver_field.get(), message_field.get()))
        send_button.grid(row=4, column=0)
        rec_button = Button(self.root, text='receive', font=('Arial', 12), command=lambda: self.enter_chat_button_on_click(True, chat_label))
        rec_button.grid(row=5, column=0)

    def send(self, receiver_name, content):
        send_message(self.client_name, receiver_name, content)



def get_messages(user_name):
    url = api + 'Server'
    json_data = req.get(url).json()
    result = []

    for i in json_data['data']:
        if i['attributes']['receiver'] == user_name:
            result.append({'sender': i['attributes']['sender'], 'content': i['attributes']['content']})


def send_message(sender, receiver, msg_content):
    url = api+'Server/send_message/'
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
    url = api + 'Server/get_messages_addressed_to'
    data = {
        "meta": {
            "method": "get_messages_addressed_to",
            "args": {
                "username": username
            }
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    return response


def login_or_register(username):
    url = api + 'Server/login_or_register_user'
    data = {
        "meta": {
            "method": "login_or_register_user",
            "args": {
                "user_name": username
            }
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    return response


if __name__ == '__main__':
    window = Window()