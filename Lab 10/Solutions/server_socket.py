from codecs import encode
import socket 
import threading
from tkinter.font import Font
import mysql.connector
from sqlalchemy.sql.expression import select

HEADER = 64
PORT = 5050
SERVER = "192.168.100.5"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="bartek",
  database="chat"
)
mycursor = mydb.cursor()


def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")

	connected = True
	myUser = ''
	mycursor.execute("UPDATE users SET isLogged = 'No'")
	mydb.commit()
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			code, msg = msg.split(";", 1)
			#login
			if code == "1":
				callback = "0"
				username, password = msg.split(";", 1)

				sql = "SELECT username, password, isLogged FROM users WHERE username = %s"
				val = (username, )
				mycursor.execute(sql, val)
				myresult = mycursor.fetchone()

				if myresult is not None and myresult[2] == "No":
					if myresult[1] == password:
						if myUser == '':
							sql = "UPDATE users SET isLogged = 'No' WHERE username = %s"
							mycursor.execute(sql,(myUser,))
						callback = "1"
						sql = "UPDATE users SET isLogged = 'Yes' WHERE username = %s"
						mycursor.execute(sql, val)
						mydb.commit()
				sql = "SELECT username FROM users WHERE isLogged = 'Yes'"
				mycursor.execute(sql)
				myresult = mycursor.fetchall()
				conn.send(callback.encode(FORMAT))
			#register
			elif code == "2":
				username, password = msg.split(";", 1)
				sql = "SELECT username FROM users WHERE username = %s"
				val = (username, )
				mycursor.execute(sql, val)
				myresult = mycursor.fetchall()
				if len(myresult) == 0:
					sql = "INSERT INTO users (username, password, isLogged) VALUES (%s, %s, %s)"
					val = (username, password, "No")
					mycursor.execute(sql, val)
					mydb.commit()
					conn.send("1".encode(FORMAT))
				else:
					conn.send("0".encode(FORMAT))
			#update
			elif code == "3":
				sql = "SELECT username FROM users WHERE isLogged = 'Yes'"
				mycursor.execute(sql)
				myresult = mycursor.fetchall()
				if myresult is not None and len(myresult) > 0:
					callback = str(len(myresult))
					for i in range(len(myresult)):
						callback += ";" + str(myresult[i][0])
					conn.send(callback.encode(FORMAT))
				else:
					conn.send("0;None".encode(FORMAT))
			#choose user
			elif code == "4":
				source, destination = msg.split(";",1)
				sql = "SELECT * FROM message WHERE (source = %s AND dest = %s) OR (source = %s AND dest = %s)"
				val = (source,destination,destination,source,)
				mycursor.execute(sql,val)
				myresult = mycursor.fetchall()
				if myresult is not None:
					callback = str(len(myresult))
					for i in range(len(myresult)):
						for j in range(6):
							callback += ";" + str(myresult[i][j])
					conn.send(callback.encode(FORMAT))
				else:
					conn.send("0;0".encode(FORMAT))
			elif code == "5":
				data = msg.split(";")
				sql = "INSERT INTO message (dest, source, text, sent) VALUES(%s, %s, %s, %s)"
				val = (data[2],data[1],data[0],data[3],)
				mycursor.execute(sql,val)
	#loguot
	if myUser == '':
		sql = "UPDATE users SET isLogged = 'No' WHERE username = %s"
		mycursor.execute(sql,(myUser,))
		mydb.commit()
	conn.close()
        

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start()