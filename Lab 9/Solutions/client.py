import tkinter as tk
from tkinter import Entry, Label, Button, Frame
import requests as req
from tkinter.ttk import Combobox

api = 'http://localhost:5000/'

#TO ADD, COMBOBOX TO SHOW ALL USERS

class Window:
    root = tk.Tk()
    root.geometry("400x200")
    client_name = ""
    client_password = ""
    entry_login_label = None
    entry_login_frame = None
    entry_password_label = None
    entry_password_frame = None

    def __init__(self):
        self.root.title('Chat')
        self.entry_login_frame = Frame(self.root)
        self.entry_login_frame.grid(row=0)
        login_label = Label(self.entry_login_frame, text='Nickname: ', font=('Arial', 12))
        self.entry_login_label = Entry(self.entry_login_frame, width=20, font=('Arial', 12))
        password_label = Label(self.entry_password_frame, text='Password: ', font=('Arial', 12))
        self.entry_password_label = Entry(self.entry_password_frame, width=20, font=('Arial', 12))
        log_in_button = Button(self.entry_login_frame, text='Log in', font=('Arial', 12), command=lambda: self.enter_chat_log_button())
        register_button = Button(self.entry_login_frame, text='Register', font=('Arial', 12), command=lambda: self.enter_chat_reg_button())

        login_label.grid(row=0, column=0)
        self.entry_login_label.grid(row=1, column=0)
        password_label.grid(row=2, column=0)
        self.entry_password_label.grid(row=3, column=0)
        log_in_button.grid(row=4, column=0)
        register_button.grid(row=5, column=0)
        self.root.mainloop()

    def enter_chat_log_button(self):
        self.client_name = self.entry_login_label.get()
        self.client_password = self.entry_password_label.get()
        response = log_in_user(self.client_name, self.client_password)
        if not response.json()['meta']['result']['result'] == 'failed':
            self.create_chat_window()

    def refresh_chat(self, chat_label, personPicked):
        chat_label.destroy()
        log_in_user(self.client_name, self.client_password)
        self.create_chat_window(personPicked)

    def enter_chat_reg_button(self):
        self.client_name = self.entry_login_label.get()
        self.client_password = self.entry_password_label.get()
        response = register_user(self.client_name, self.client_password)
        print(response.json())
        if not response.json()['meta']['result']['result'] == 'failed':
           self.create_chat_window()

    def create_chat_window(self, personPicked=0):
        self.entry_login_frame.destroy()
        nickname_label = Label(self.root, text='Your nickname: '+self.client_name, font=('Arial', 12))
        nickname_label.grid(row=0, column=0)
        chat_label = Label(self.root, text='', background='white', font=('Arial', 12))
        list_of_messages = get_messages_addressed_to(self.client_name).json()['meta']['result']['result']
        if not personPicked == 0:
            list_of_messages_to_person_picked = get_messages_addressed_to(personPicked).json()['meta']['result']['result']
        chat_window = ''
        if not personPicked == 0:
            for i in list_of_messages_to_person_picked:
                if i['sender']==self.client_name:
                    chat_window += '\n'+i['sender']+": "+i['content']
        if personPicked=='allchat':
            print("XD")
            list_of_m = get_messages_from_grpchat().json()['meta']['result']['result']
            print(list_of_m)
            for i in list_of_m:
                chat_window += '\n' + i +": " + (list_of_m[i][0]['content'])
        else:
            for i in list_of_messages:
                if i['sender']==personPicked:
                    chat_window += '\n'+i['sender']+": "+i['content']

        chat_label.configure(text=chat_window)
        chat_label.grid(row=1, column=0)

        message_field = Entry(self.root, background='white', width=20, font=('Arial', 12))
        message_field.grid(row=2, column=0)
        comboUser = Combobox(self.root, font=("Arial Bold", 16), state='readonly')
        comboUser["values"] = get_all_users().json()['meta']['result']['result']
        print(get_all_users().json())
        comboUser.current(0)
        comboUser.grid(row=0, column=1, padx=(2, 2)) 

        receiver_field = Entry(self.root, background='white', width=20, font=('Arial', 12))
        receiver_field.grid(row=3, column=0)
        send_button = Button(self.root, text='send', font=('Arial', 12), command=lambda: self.send(comboUser.get(), message_field.get(), chat_window))
        send_button.grid(row=4, column=0)
        rec_button = Button(self.root, text='receive', font=('Arial', 12), command=lambda: self.refresh_chat(chat_label, comboUser.get()))
        rec_button.grid(row=5, column=0)

    def send(self, receiver_name, content, chat_window):
        #chat_window += '\n'+self.client_name+": "+content
        
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

def get_all_users():
    url = api + 'Server/get_all_users'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.get(url, headers=headers)
    return response

def get_messages_from_grpchat():
    url = api + 'Server/get_messages_from_grpchat'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.get(url, headers=headers)
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


def log_in_user(username, password):
    url = api + 'Server/log_in_user'
    data = {
        "meta": {
            "method": "log_in_user",
            "args": {
                "user_name": username,
                "password": password
            }
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    return response

def register_user(username, password):
    url = api + 'Server/register_user'
    data = {
        "meta": {
            "method": "register_user",
            "args": {
                "user_name": username,
                "password": password
            }
        }
    }
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = req.post(url, json=data, headers=headers)
    return response


if __name__ == '__main__':
    window = Window() 