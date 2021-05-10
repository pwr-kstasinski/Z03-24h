from tkinter import *
import tkinter as tk
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



global_userID = None
global_userNICKNAME = None








def logIn(user_id):
    global global_userID
    global global_userNICKNAME
    label_text = "\t\t\t\t\t\t\t\t\t\t\t"  # clean space
    Label(root, text=label_text).grid(row=6, column=0, columnspan=3, sticky='N')
    label_text = "Error. Enter User ID"
    if not user_id == '':
        text = {"id": user_id}
        r = requests.post("http://127.0.0.1:5000/users/login", json=text)

        if r.status_code == 200:        # OK
            global_userID = r.json()['id']
            global_userNICKNAME = r.json()['nickname']
            label_text = "Logged in user: " + str(r.json()['nickname']) + ", ID: " + str(r.json()['id'])
            loggedGUI()
            swap_frame(logged_frame)
        else:
            label_text = "There is no such user with this ID"

    Label(root, text=label_text).grid(row=6, column=0, columnspan=3, sticky='N')
  #  loggedGUI()
  #  swap_frame(logged_frame)

def register(user_id, user_nickname):
    label_text = "\t\t\t\t\t\t\t\t\t\t\t"             # clean space
    Label(root, text=label_text).grid(row=6, column=0, columnspan=3, sticky='N')
    label_text = "Error. Enter both User ID and User Nickname"
    if not (user_id == '' or user_nickname == ''):

        text = {"id": user_id, "nickname": user_nickname}
        r = requests.post("http://127.0.0.1:5000/users/new", json=text)

        if r.status_code == 200:        # OK
            label_text = "Added user: " + str(r.json()['nickname']) + ", ID: " + str(r.json()['id'])
        else:
            label_text = "This User ID is already taken"

    Label(root, text=label_text).grid(row=6, column=0, columnspan=3, sticky='N')





def logOut():
    global global_userID
    global global_userNICKNAME
    global_userID = None
    global_userNICKNAME = None
    swap_frame(root)




def sendMessage(destination_id, message):
    pass



# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________


def loggedGUI():
    x_of_button = 20
    y_of_button = 10
    label_nickname = Label(logged_frame, text="Logged in as: " + global_userNICKNAME)
    label_destinationID = Label(logged_frame, text="Destination User ID")

    button_logout = Button(logged_frame, text="LOGOUT", width=x_of_button, bg="red", command=lambda: logOut())
    label_message = Label(logged_frame, text="Message:")
    entry_destinationID = Entry(logged_frame, width=x_of_button)
    entry_message = Entry(logged_frame, width=x_of_button*3)
    button_send = Button(logged_frame, text="SEND", width=x_of_button, pady=y_of_button, bg="white", command=lambda: sendMessage(entry_destinationID, entry_message))

    
    label_chat = Label(logged_frame, height=80)

    label_chat.place(relwidth=10, rely=0.825) #grid(row=0, column=1, columnspan=3)


    current_row = 0
    label_message.grid(row=1, column=0, columnspan=1)
    entry_message.grid(row=1, column=1, columnspan=3, sticky='W')

    button_send.grid(row=2, column=0, rowspan=2, sticky='NE')
    label_destinationID.grid(row=2, column=1, columnspan=1, sticky='N')
    entry_destinationID.grid(row=3, column=1, columnspan=1, sticky='N')
    label_nickname.grid(row=2, column=3, columnspan=1)
    button_logout.grid(row=3, column=3, sticky='NE')
























def startGUI():
    # ___________________________________________________ creating gui elements
    x_of_button = 20
    y_of_button = 10

    label_id = Label(root, text="User ID")
    label_id2 = Label(root, text="User ID")
    label_nickname = Label(root, text="User Nickname")
    label_login = Label(root, text="Login with User ID")
    entry_login = Entry(root, width=50)
    button_login = Button(root, text="LOG IN", width=x_of_button, pady=y_of_button, bg="lightblue", command=lambda: logIn(entry_login.get()))
    label_or = Label(root, text="or")
    label_register = Label(root, text="Register new user using ID and Nickname")
    entry_register_id = Entry(root, width=50)
    entry_register_nickname = Entry(root, width=50)
    button_register = Button(root, text="REGISTER", width=x_of_button, pady=y_of_button, bg="red", command=lambda: register(entry_register_id.get(), entry_register_nickname.get()))

    # ___________________________________________________ showing gui
    label_login.grid(row=0, column=0, columnspan=3, sticky='N')
    label_id.grid(row=1, column=0, sticky='W')
    entry_login.grid(row=1, column=1, sticky='W')
    button_login.grid(row=1, column=2, sticky='W')

    label_or.grid(row=2, column=0, columnspan=3, sticky='N')

    label_register.grid(row=3, column=0, columnspan=3, sticky='N')
    label_id2.grid(row=4, column=0, sticky='W')
    entry_register_id.grid(row=4, column=1, sticky='W')
    button_register.grid(row=4, column=2, sticky='W', rowspan=2)
    label_nickname.grid(row=5, column=0, sticky='W')
    entry_register_nickname.grid(row=5, column=1, sticky='W')


if __name__ == "__main__":
    startGUI()

root.mainloop()
