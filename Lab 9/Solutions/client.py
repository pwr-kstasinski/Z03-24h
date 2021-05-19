import requests
from requests.api import request
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


BASE = "http://127.0.0.1:5000"

myUsername = ''
myPassword = ''
myMessages = {}
logged = False

#button comands
def log_popup():
    logWindow = tk.Toplevel()
    logWindow.geometry('200x100')

    logEntry = tk.Entry(logWindow, bg='gray')
    logEntry.pack()
    pasEntry = tk.Entry(logWindow, bg='gray')
    pasEntry.pack()

    logWarning = tk.Label(logWindow, text='')
    logWarning.pack()
    def changeLabel(newText):
        logWarning["text"] = newText

    bt_logIn = tk.Button(logWindow, text="Login", command=lambda: logWindow.destroy() if logMeIn(logEntry.get(), pasEntry.get()) else changeLabel("Wrong input!"))
    bt_reg = tk.Button(logWindow, text="Register", command=lambda: changeLabel("User registred succesful") if registerMe(logEntry.get(), pasEntry.get()) else changeLabel("User already exists!"))
    bt_logIn.pack(side='bottom')
    bt_reg.pack(side='bottom')




#window base
HEIGHT = 700
WIDTH = 800
root = tk.Tk()
root.geometry('700x800')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#chatbox
chatFrame = tk.Frame(root, bg='blue')
chatFrame.place(relx=0.3, rely=0.1, relwidth=0.6, relheight=0.8)

#messeges
scrollbar = tk.Scrollbar(chatFrame)
scrollbar.place(relx=0.95, rely=0, relwidth=0.05, relheight=0.8)
msgbox = tk.Text(chatFrame)
msgbox.place(relx=0, rely=0, relwidth=0.95, relheight=0.8)
msgbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=msgbox.yview)
msgbox['state'] = 'disabled'


#sending message
msgText = tk.Text(chatFrame)
msgText.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

bt_msg_send = tk.Button(chatFrame, text='Send', bg='gray', command=lambda: msgText.delete('1.0', tk.END) if sendMessage(msg_dest_entry.get(), msgText.get("1.0", 'end-1c'))else False)
bt_msg_send.place(relx=0.9, rely=0.9, relwidth=0.1, relheight=0.1)

msg_dest_entry = tk.Entry(chatFrame, bg='gray')
msg_dest_entry.place(relx=0, rely=0.85, relheight=0.05)

#login
userLeb = tk.Label(root, text = "My username:"+ myUsername)
userLeb.pack(side='top')

bt_log = tk.Button(canvas, text='login', bg='gray', command=lambda: log_popup())
bt_log.pack()

#online users
onlineFrame = tk.Frame(root, bg='lightblue')
onlineFrame.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.8)

onlineLeb = tk.Label (onlineFrame, text="Online Users")
onlineLeb.place(relx=0, rely=0, relwidth=1, relheight=0.05)

onlineText =tk.Text(onlineFrame)
onlineText.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)
onlineText['state'] = 'disabled'

#methods
def logMeIn(username, password):
    response = requests.put(BASE + "/login", {"username": username, "password": password, 'isLogged': 'Yes'})
    if response.status_code == 400:
        return False
    else:
        global myUsername
        global myPassword
        myUsername = username
        myPassword = password
        userLeb['text'] = "My username: " + username
        return True

def logMeOut():
    global myUsername
    global myPassword
    requests.put(BASE + "/login", {"username": myUsername, "password": myPassword, 'isLogged': 'No'})
    myUsername = ''
    myPassword = ''
    root.destroy()

def registerMe(username, password):
    response = requests.post(BASE + "/login", {"username": username, "password": password, 'isLogged': 'No'})
    if response.status_code == 400:
        return False
    else:
        return True

def sendMessage(destination, text):
    response = requests.post(BASE + "/msg", {"source": myUsername, "destination": destination, "text": text})
    if response.status_code==200:
        myMessages[response] = {"source": myUsername, "destination": destination, "text": text}
        refresh()
        return True
    else:
        return False

def reciveMessage():
    response = requests.put(BASE + "/msg", {"username": myUsername}) 
    if response.status_code==200:
        for msg in response.json():
            myMessages[response] = {"source": msg['source'], "destination": msg['destination'], "text": msg['text']}

def getOnlineUsers():
    response = requests.get(BASE + "/login").json()
    return response['onlineUsers'].keys()

def refresh():
    reciveMessage()
    global myMessages
    msgbox['state'] = 'normal'
    for id, msgs in myMessages.items():
        if msgs['destination'] == myUsername:
            dest ='Me'
        else:
            dest = msgs['destination']

        if msgs['source'] == myUsername:
            src ='Me'
        else:
            src = msgs['source']

        msgbox.insert(1.0, f"From: {src}    To:{dest}\n{msgs['text']}\n\n")
    myMessages = {}
    msgbox['state'] = 'disabled'

    onlineText['state'] = 'normal'
    onlineText.delete('1.0', tk.END)
    onlineUsers = getOnlineUsers()
    for user in onlineUsers:
        if user != myUsername:
            onlineText.insert(tk.END, user+"\n")

    onlineText['state'] = 'disabled'

    

bt_ref = tk.Button(canvas, text='Refresh', bg='gray', command=lambda: refresh())
bt_ref.pack(side='bottom')
root.protocol("WM_DELETE_WINDOW", logMeOut)
root.mainloop()