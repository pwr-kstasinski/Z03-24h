import tkinter as tk
from tkinter import *
from tkinter import messagebox
from api_client import send_message, get_users, get_conversation, mark_as_seen, get_number_of_unread_messages, \
    set_status
import time
import datetime
import socketio

default_font = ('Arial', 12)
big_font = ('Arial', 16)

#sio = socketio.Client()
class ChatWindow:
    
    sio = socketio.Client()
    
    def __init__(self, cli_name, cli_id, rec_name):
        #sio = socketio.Client()
        
    
        

        set_status(cli_id, True)
        self.client_name = cli_name 
        self.client_id = cli_id
        self.receiver_name = rec_name
        self.conversation_list = {}  
        self.user_list = [] 

        

        

        self.frame_chat = None  
        self.frame_users = None  
        self.frame_message = None  
        self.message_entry = None 
        self.receiver_name_label = None  
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title(f'{self.client_name}\'s chat')

        button_global = Button(text='global', font=default_font, command=lambda: self.on_global_button_click())
        button_global.grid(row=0)

        button_refresh = Button(text='refresh', font=default_font, command=lambda: self.refresh())
        button_refresh.grid(row=2, column=2)

        self.receiver_name_label = Label(self.root, text=f'chat with {self.receiver_name}', font=big_font)
        self.receiver_name_label.grid(row=0, column=1, sticky='w')

        self.init_chat_window()

        self.init_user_list()

    @sio.event
    def messages_displayed(self, data):
        print('messages displayed')
        receiver = data['receiver']
        sender = data['sender']
        if receiver == self.client_name or sender == self.client_name:
            self.update_all_messages()
            self.get_all_users()
            self.sort_user_list()
            self.update_user_list()
            if sender == self.receiver_name:
                self.update_chat_window()
    @sio.event
    def login_or_register(self):
        print('User logged in')
        self.get_all_users()
        self.sort_user_list()
        self.update_user_list()

    @sio.event
    def new_message(self, data):
        print('new message')
        receiver = data['receiver']
        if receiver == self.client_name:
            sender = data['sender']
            self.update_all_messages()
            self.get_all_users()
            self.sort_user_list()
            self.update_user_list()
            if sender == self.receiver_name:
                self.update_chat_window()
    def init_user_list(self):
        frame_canvas = Frame(self.root, height=350)
        frame_canvas.grid(row=1, column=0, pady=5, sticky='nws')

        canvas = Canvas(frame_canvas, bg="white", width=200)
        canvas.grid(row=0, column=0, sticky="news")

        vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        self.frame_users = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=self.frame_users, anchor='w')

        self.get_all_users()  
        self.sort_user_list()  

        self.update_user_list()  

        self.frame_users.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def update_user_list(self):
        for widget in self.frame_users.winfo_children():
            widget.destroy()

        for i in range(len(self.user_list)):
            username = self.user_list[i]['name']
            user_description = f'{username}\n'

            if username != self.client_name:
                status = 'offline'
                if self.user_list[i]['status']:
                    status = 'online'
                user_description += f'status: {status}\n'

                unread_messages = self.user_list[i]['unread_mess']
                user_description += f'unread mess: {unread_messages}'

                Button(self.frame_users,
                       text=user_description,
                       font=default_font, pady=5, justify='left',
                       command=lambda c=i: self.change_receiver(self.user_list[c]['name']),
                       width=22).grid(row=i)

        self.frame_users.update_idletasks()
        canvas = self.frame_users.master
        canvas.config(scrollregion=canvas.bbox("all"))

    def init_chat_window(self):
        chat_frame_canvas = Frame(self.root, bg='powder blue')
        chat_frame_canvas.grid(row=1, column=1, pady=5, sticky='nws')

        chat_canvas = Canvas(chat_frame_canvas, bg="powder blue", width=380)
        chat_canvas.grid(row=0, column=0, sticky="news")

        chat_scrollbar = Scrollbar(chat_frame_canvas, orient="vertical", command=chat_canvas.yview, name='scbar')
        chat_scrollbar.grid(row=0, column=1, sticky='ns')
        chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

        self.frame_chat = Frame(chat_canvas, bg="white")
        chat_canvas.create_window((0, 0), window=self.frame_chat, anchor='nw', width=380)

        self.sort_all_messages()
        self.update_chat_window()

        self.frame_chat.update_idletasks()
        chat_canvas.config(scrollregion=chat_canvas.bbox("all"))

        self.frame_message = Frame(self.root)
        self.frame_message.grid(row=2, column=1, sticky='w')
        self.message_entry = Entry(self.frame_message, font=default_font, width=30)
        self.message_entry.grid(row=0, column=0)
        Button(self.frame_message, text='send', font=default_font,
               command=lambda: self.send(self.receiver_name, self.message_entry.get())).grid(row=0, column=1)

    def update_chat_window(self, update_notification=True):
        self.frame_chat.grid_forget()

        for widget in self.frame_chat.winfo_children():
            widget.destroy()

        if self.receiver_name in self.conversation_list:
            conversation = self.conversation_list[self.receiver_name]
            messages_to_mark = []
            for i in range(len(conversation)):
                message_string = ''
                msg_box_label = Label(self.frame_chat, anchor='w', justify='left')
                self.frame_chat.columnconfigure(0, weight=1)

                id = conversation[i]['id']
                sender = conversation[i]['sen']
                receiver = conversation[i]['rec']
                dtime = conversation[i]['dtime']
                dtime = dtime[:19]
                content = conversation[i]['cont']
                seen = conversation[i]['read']

                if sender == self.client_name:
                    message_string += "You at " + str(dtime) + '\n'
                    message_string += content + '\n'
                    if receiver != 'global':
                        if seen:
                            message_string += 'seen'
                        else:
                            message_string += 'not seen'
                    msg_box_label.configure(text=message_string, bg='sky blue')
                    msg_box_label.grid(row=i, sticky='e')
                else:
                    message_string += str(sender) + " at " + str(dtime) + '\n'
                    message_string += content
                    msg_box_label.configure(text=message_string, bg='cyan')
                    msg_box_label.grid(row=i, sticky='w')
                    #mark_as_seen(id)  # <====================================setting seen parameter to True
                    if not seen:
                        messages_to_mark.append(id) #mess_id 
            if len(messages_to_mark) > 0:
                #mark_as_seen(messages_to_mark, self.client_name, self.receiver_name)
                for mess_id in messages_to_mark:
                    mark_as_seen(mess_id)
            elif update_notification:
                self.update_chat_window(False)

            self.frame_chat.update_idletasks()
            chat_canvas = self.frame_chat.master
            chat_canvas.config(scrollregion=chat_canvas.bbox("all"))

    def get_all_messages(self):
        all_messages = get_conversation(self.client_name)
        return all_messages

    def sort_all_messages(self):
        messages = self.get_all_messages()
        self.conversation_list['global'] = []

        for i in range(len(messages['id'])):
            id = messages['id'][i]
            sender = messages['sen'][i]
            receiver = messages['rec'][i]
            content = messages['cont'][i]
            datetime = messages['dtime'][i]
            read = messages['read'][i]

            mess_tuple = {'id': id, 'rec': receiver, 'sen': sender, 'cont': content, 'dtime': datetime, 'read': read}

            if sender == self.client_name:
                if not receiver in self.conversation_list:
                    self.conversation_list[receiver] = []
                self.conversation_list[receiver].append(
                    mess_tuple
                )
            elif receiver == 'global':
                self.conversation_list['global'].append(
                    mess_tuple
                )
            else:
                if not sender in self.conversation_list:
                    self.conversation_list[sender] = []
                self.conversation_list[sender].append(
                    mess_tuple
                )

    def get_all_users(self):
        users = get_users()
        self.user_list.clear()
        for i in range(len(users)):
            username = users[i]["attributes"]["name"]
            if username != self.client_name:
                id = users[i]["id"]
                status = users[i]["attributes"]["is_online"]
                unread_mess = self.number_of_unread_messages(username)
                last_mess = str(datetime.datetime.fromtimestamp(0))
                if username in self.conversation_list:
                    last_mess = self.conversation_list[username][-1]['dtime']
                user = {'id': id, 'name': username, 'status': status, 'unread_mess': unread_mess, 'last_mess': last_mess}
                self.user_list.append(user)

    def sort_user_list(self):
        sorted_list = sorted(self.user_list, key=lambda u: u['last_mess'], reverse=True)
        sorted_list = sorted(sorted_list, key=lambda u: u['status'], reverse=True)
        self.user_list = sorted_list

    def number_of_unread_messages(self, receiver_name):
        if receiver_name in self.conversation_list:
            count = 0
            conversation = self.conversation_list[receiver_name]
            for m in conversation:
                if m['sen'] != self.client_name:
                    if not m['read']:
                        count += 1
            return count
        else:
            return 0

    def on_global_button_click(self):
        self.update_receiver('global')
        self.update_receiver_label()
        self.update_chat_window()

    def change_receiver(self, receiver_name):
        self.update_receiver(receiver_name)
        self.update_receiver_label()
        self.update_chat_window()
        for m in self.user_list:
            if m['name'] == self.receiver_name:
                m['unread_mess'] = 0
        self.sort_user_list()
        self.update_user_list()

    def send(self, receiver_name, content):
        send_message(self.client_name, receiver_name, content)
        self.conversation_list.clear()
        self.sort_all_messages()
        self.get_all_users()
        self.sort_user_list()
        self.update_user_list()
        self.update_chat_window()
        self.message_entry.delete(0, tk.END)

    def update_receiver(self, new_receiver):
        self.receiver_name = new_receiver

    def update_receiver_label(self):
        self.receiver_name_label.configure(text=f'chat with {self.receiver_name}')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            set_status(self.client_id, False)
            self.root.destroy()

    def refresh(self):
        self.get_all_users()
        self.sort_all_messages()
        self.update_user_list()
        self.update_chat_window()


    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    w = ChatWindow("User2", 3, "")
    w.start()
    #w.sio.on('w', w.sio)
    w.sio.connect('http://127.0.0.1:5000')


if __name__ == '__main__':
    main()