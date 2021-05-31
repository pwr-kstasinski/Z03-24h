import tkinter as tk
import socket
import datetime

from sqlalchemy.sql.expression import false, true

SERVER = "192.168.100.5"
PORT = 5050
HEADER = 64 
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
HEIGHT = 600
WIDTH = 500

myUsername = ""
myLink = "None"
myMessage = ""
isLogged = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	callback = msg[0] 
	if msg[0] == 4:
		print(msg)
		print(message)
		print(msg_length)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	if callback == 4:
		print(send_length)
	client.send(send_length)
	client.send(message)
	receiveMessage = client.recv(2048).decode(FORMAT)
	#login
	if callback == "1":
		if receiveMessage == "0":
			return False
		global myUsername 
		myUsername = msg.split(";")[1]
		usernameLabel['text'] = f"My username: {myUsername}"
		return True
	#register
	elif callback == "2":
		if receiveMessage == "0":
			return False
		return True
	#update
	elif callback == "3":
		activeUsers = receiveMessage.split(";")
		counter = int(activeUsers[0])
		OnlineLabel['text'] = f"Online users: {counter}"
		onlineText['state'] = 'normal'
		onlineText.delete(1.0,tk.END)
		for i in range(1, counter + 1):
			onlineText.insert(1.0, f"{activeUsers[i]}\n")
		onlineText['state'] = 'disabled'
		return True
	#show messages
	elif callback == "4":
		messages = receiveMessage.split(";")
		counter = int(messages[0])
		messageBox['state'] = 'normal'
		messageBox.delete(1.0, tk.END)
		for i in range(1, counter * 5 + 1, 6):
			messageBox.insert(1.0, f"message from{messages[i+2]} to {messages[i+1]} at {messages[i+4]}:\n {messages[i+3]}")
		messageBox['state'] = 'disabled'

	#sent message(text, source, destination, date)
	elif callback == "5":
		pass
	
	return True

def update():
	send("3;0")
	root.after(1000, update) # run itself again after 1000 ms

#popup window
def login_pop():
	logWindow = tk.Toplevel()
	logWindow.geometry('200x100')

	loginEntry = tk.Entry(logWindow, bg="gray")
	loginEntry.pack()
	passwordEntry = tk.Entry(logWindow, bg="gray")
	passwordEntry.pack()
	
	popWarning = tk.Label(logWindow, text="")
	popWarning.pack()
	
	def changeLabel(newText):
		popWarning['text'] = newText

	buttonLogin = tk.Button(logWindow, text="Login", command=lambda: logWindow.destroy() if send("1;" + loginEntry.get() + ";" + passwordEntry.get()) else changeLabel("Wrong data!"))
	buttonRegister = tk.Button(logWindow, text="Register", command=lambda: changeLabel("User registred succesfully") if send("2;" + loginEntry.get() + ";" + passwordEntry.get()) else changeLabel("User already exists!"))
	buttonRegister.pack(side='bottom')
	buttonLogin.pack(side='bottom')

#choosing destination
def chooseLink():
	global myLink
	myLink = chooseUser.get()
	sourceLabel['text'] = f"Conversation with: {myLink}"
	global myUsername
	call = "4;" + myUsername + ";" + myLink
	send(call)

#sending message
def sendMessage():
	myMessage = "5;" + messageText.get()
	now = datetime.datetime.now()
	formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
	global myLink
	myMessage += ";" + myUsername + ";" + myLink + ";" + formatted_date
	print(myMessage)
	send(myMessage)

#window
root = tk.Tk()
root.geometry('600x500')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#onlineFrame
onlineFrame = tk.Frame(root)
onlineFrame.place(relx=0.05, rely=0, relwidth=0.2, relheight=0.9)

OnlineLabel = tk.Label(onlineFrame, text="Online users: 0")
OnlineLabel.place(relx=0, rely=0.05, relwidth=1, relheight=0.05)

usernameLabel = tk.Label(root, text = "My username: ")
usernameLabel.place(relx=0, rely=0, relwidth=0.3, relheight=0.05)


onlineText = tk.Text(onlineFrame)
onlineText.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
onlineText['state'] = 'disabled'

#chatFrame
chatFrame = tk.Frame(root)
chatFrame.place(relx=0.3, rely=0.1, relwidth=0.65, relheight=0.9)

chooseUser = tk.Entry(chatFrame)
chooseUser.place(relx=0, rely=0, relwidth=1, relheight=0.05)

scrollbar = tk.Scrollbar(chatFrame)
scrollbar.place(relx=0.95, rely=0.15, relwidth=0.05, relheight=0.75)
messageBox = tk.Text(chatFrame)
messageBox.place(relx=0, rely=0.15,relwidth=0.95, relheight=0.65)
messageBox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=messageBox.yview)
messageBox['state'] = 'disabled'

sourceLabel = tk.Label(chatFrame, text = "Conversation with: ")
sourceLabel.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.05,)

messageText = tk.Entry(chatFrame)
messageText.place(relx=0, rely=0.85, relheight=0.1, relwidth=0.9)


#buttons
buttonMessage = tk.Button(chatFrame, bg="gray", text="Send message", command=lambda:sendMessage())
buttonMessage.place(relx=0, rely=0.95, relheight=0.05, relwidth=0.5)

buttonUser = tk.Button(chatFrame, bg="gray", text="Choose user", command=lambda:chooseLink() )
buttonUser.place(relx=0,rely=0.05, relwidth=0.5, relheight=0.05)

buttonLogin = tk.Button(root, bg="gray", text="Login",command= lambda: login_pop())
buttonLogin.place(relx=0.45, rely=0.02, relwidth=0.3,relheight=0.05)


update()
root.mainloop()
