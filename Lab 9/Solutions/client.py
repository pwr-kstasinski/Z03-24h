from tkinter import *
import tkinter as tk
from tkinter import scrolledtext

import requests
import json
from flask import Flask, jsonify, current_app

def swap_frame(frame):
    frame.tkraise()



window = Tk()
window.title("Komunikator")
# this removes the maximize button
window.resizable(0, 0)

logged_frame = Frame(window)
root = Frame(window)

#root.title("Komunikator")
# this removes the maximize button
#root.resizable(0, 0)
logged_frame.grid(row=0, column=0, sticky='news')
root.grid(row=0, column=0, sticky='news')



global_Login = None
global_last_message_id = 0







def logIn(login, password):
    global global_Login
    label_text = "\t\t\t\t\t\t\t\t\t\t\t"  # clean space
    Label(root, text=label_text).grid(row=7, column=0, columnspan=3, sticky='N')
    label_text = "Error. Enter both Login and Password to log in"
    if not (login == '' or password == ''):
        text = {"login": login, "password": password}
        r = requests.post("http://127.0.0.1:5000/users/login", json=text)

        if r.status_code == 200:        # OK
            global_Login = r.json()['login']
            label_text = "'" + str(r.json()['login'] + "' has been logged out")
            loggedGUI()
            swap_frame(logged_frame)
        else:
            label_text = "There is no such user with this Login and Password"

    Label(root, text=label_text).grid(row=7, column=0, columnspan=3, sticky='N')
  #  loggedGUI()
  #  swap_frame(logged_frame)

def register(login, password):
    label_text = "\t\t\t\t\t\t\t\t\t\t"             # clean space
    Label(root, text=label_text).grid(row=7, column=0, columnspan=3, sticky='N')
    label_text = "Error. Enter both Login and Password to register"
    if not (login == '' or password == ''):

        text = {"login": login, "password": password}
        r = requests.post("http://127.0.0.1:5000/users/new", json=text)

        if r.status_code == 200:        # OK
            label_text = "Added user: " + str(r.json()['login'])
        else:
            label_text = "This Login is already taken"

    Label(root, text=label_text).grid(row=7, column=0, columnspan=3, sticky='N')





def logOut():
    global global_Login
    global global_last_message_id
    text = {"login": global_Login}
    requests.put("http://127.0.0.1:5000/users/logout", json=text)
    global_Login = None
    global_last_message_id = 0
    swap_frame(root)











def showLoggedInUsers():
    r = requests.get("http://127.0.0.1:5000/users/loggedin").json()['logged_in_users']
    newWindow = Toplevel(logged_frame)
    for user in r:
        Label(newWindow, text=user).pack()



# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________


def loggedGUI():
    x_of_button = 20
    y_of_button = 10
    label_nickname = Label(logged_frame, text="Logged in as: " + global_Login)
    label_destinationID = Label(logged_frame, text="Destination User Login")

    button_logout = Button(logged_frame, text="LOGOUT", width=x_of_button, bg="red", command=lambda: logOut())
    label_message = Label(logged_frame, text="Message:")
    entry_destinationID = Entry(logged_frame, width=x_of_button)
    entry_message = Entry(logged_frame, width=x_of_button*3)
    button_send = Button(logged_frame, text="SEND", width=x_of_button, pady=y_of_button, bg="white", command=lambda: sendMessage(entry_destinationID.get(), entry_message.get()))
    button_show_logged_in_users = Button(logged_frame, text="Logged in users", width=x_of_button, bg="white", command=lambda: showLoggedInUsers())
 #   label_chat = Label(logged_frame, height=80)

    button_update_messages = Button(logged_frame, text="UPDATE MESSAGES", width=x_of_button, bg="yellow", command=lambda: getMessage())
    text_messages = scrolledtext.ScrolledText(logged_frame, wrap=WORD) #, state='disabled')
    text_messages.grid(row=0, columnspan=3)

 #   label_chat.place(relwidth=10, rely=0.825) #grid(row=0, column=1, columnspan=3)



    current_row = 0
    button_show_logged_in_users.grid(row=30, column=0, sticky='W')
    label_message.grid(row=10, column=0, columnspan=1, sticky='E')
    entry_message.grid(row=10, column=1, columnspan=3, sticky='E')

    # button_send.grid(row=20, column=0, rowspan=2, sticky='NW')
    # label_destinationID.grid(row=20, column=1, columnspan=1, sticky='N')
    # entry_destinationID.grid(row=30, column=1, columnspan=1, sticky='N')
    button_send.grid(row=20, column=1)
    button_update_messages.grid(row=20, column=2, sticky='NW')
    label_destinationID.grid(row=10, column=0, columnspan=1, sticky='W')
    entry_destinationID.grid(row=20, column=0, columnspan=1, sticky='W')
    label_nickname.grid(row=20, column=2, sticky='SE')
    button_logout.grid(row=30, column=2, sticky='NE')

    def getMessage():
        global global_last_message_id
        global global_Login
        text = {"id": global_last_message_id, "login": global_Login}
        messages = requests.post("http://127.0.0.1:5000/message/get", json=text)
     #   for message in messages:
     #   print(messages.json())
      #  for i in range(len(messages.json())):
        for message in messages.json():
     #       print(messages[i])
            global_last_message_id = message['message_id'] + 1
            if message['destination_login'] == '':                       # wiadomosc do wszystkich jakos zaznacza ze nie tylko do odbiorcy (tutaj strzalka)
                text_messages.insert('insert', "\n" + str(message['from_login']) + ' -> Everyone' + ': ' + str(message['message']))
            else:
                text_messages.insert('insert', "\n" + str(message['from_login']) + ': ' + str(message['message']))
     #   print("\nGLOBAL="+str(global_last_message_id))


    def sendMessage(destination_login, message):
        global global_Login
        global global_last_message_id
        text2 = {"message_data": message, "from_login": global_Login, "destination_login": destination_login}
        print(text2)
        r = requests.post("http://127.0.0.1:5000/message/send", json=text2)
    #    text_messages.insert('insert', "\n" + global_Login + ' -> ' + destination_login + ': ' + message)           # pokaz tez wiadomosci wysylane do innych
    #    global_last_message_id += 1
        getMessage()














def startGUI():
    # ___________________________________________________ creating gui elements
    x_of_button = 20
    y_of_button = 10

    label_login = Label(root, text="Login")
    label_login2 = Label(root, text="Login")
    label_nickname = Label(root, text="Password")
    label_nickname2 = Label(root, text="Password")
    label_login_string = Label(root, text="Login")
    entry_login = Entry(root, width=50)
    entry_password = Entry(root, width=50, show='*')
    button_login = Button(root, text="LOG IN", width=x_of_button, pady=y_of_button, bg="lightgreen", command=lambda:
                                                                    logIn(entry_login.get(), entry_password.get()))
    label_or = Label(root, text="or")
    label_register = Label(root, text="Register new user")
    entry_register_id = Entry(root, width=50)
    entry_register_nickname = Entry(root, width=50, show='*')
    button_register = Button(root, text="REGISTER", width=x_of_button, pady=y_of_button, bg="red", command=lambda:
                                                    register(entry_register_id.get(), entry_register_nickname.get()))

    # ___________________________________________________ showing gui
    label_login_string.grid(row=0, column=0, columnspan=3, sticky='N')
    label_login.grid(row=1, column=0, sticky='W')
    label_nickname2.grid(row=2, column=0, sticky='W')
    entry_login.grid(row=1, column=1, sticky='W')
    entry_password.grid(row=2, column=1, sticky='W')
    button_login.grid(row=1, column=2, sticky='W', rowspan=2)

    label_or.grid(row=3, column=0, columnspan=3, sticky='N')

    label_register.grid(row=4, column=0, columnspan=3, sticky='N')
    label_login2.grid(row=5, column=0, sticky='W')
    entry_register_id.grid(row=5, column=1, sticky='W')
    button_register.grid(row=5, column=2, sticky='W', rowspan=2)
    label_nickname.grid(row=6, column=0, sticky='W')
    entry_register_nickname.grid(row=6, column=1, sticky='W')


if __name__ == "__main__":
    startGUI()

root.mainloop()
text = {"login": global_Login}
requests.put("http://127.0.0.1:5000/users/logout", json=text)            # po wyjsciu z programu bez wylogowania wyloguje samo