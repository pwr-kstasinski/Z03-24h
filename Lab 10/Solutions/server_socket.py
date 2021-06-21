from codecs import encode
import socket 
import threading
from tkinter.font import Font
import mysql.connector
from sqlalchemy.sql.expression import select

HEADER = 64
PORT = 5050
SERVER = "192.168.0.13"
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
	#mycursor.execute("UPDATE users SET isLogged = 'No'")
	#mydb.commit()

	while connected:
		#decoding
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
						myUser = username
						mydb.commit()
		
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
				#received
				values = msg.split(";")
				sql = "SELECT source, id FROM message WHERE dest = %s ORDER BY id DESC"
				val = (values[1], )
				mycursor.execute(sql,val)
				received = mycursor.fetchall()

				sql = "SELECT dest, id FROM message WHERE source = %s ORDER BY id DESC"
				val = (values[1], )
				mycursor.execute(sql,val)
				sent = mycursor.fetchall()
				for i in sent:
					if i not in received:
						received.append(i)
				
				myresult = []
				results = sorted(received, key= lambda tup: tup[1], reverse=True)
				for i in results:
					if i[0] not in myresult:
						myresult.append(i[0])
				sql = "SELECT username FROM users WHERE isLogged = 'Yes'"
				mycursor.execute(sql)
				recent = mycursor.fetchall()
	
				for i in recent:
					if i[0] not in myresult:
						myresult.append(i[0])

				#lista aktywności
				#lista wiadomości		
				myresult.reverse()
				users = len(myresult)
				activity = []
				messages = []

				for i in myresult:
					sql = "SELECT isLogged FROM users WHERE username = %s"
					val = (i,)
					mycursor.execute(sql, val)
					recent = mycursor.fetchall()
					activity.append(recent[0])
				
					sql = "SELECT id FROM message WHERE dest = %s AND source = %s AND id > %s"
					val = (values[1], i, values[0])
					mycursor.execute(sql, val)
					recent = mycursor.fetchall()
					messages.append(str(len(recent)))


				myresult.extend(activity)
				myresult.extend(messages)
			
				if myresult is not None and len(myresult) > 0:
					callback = str(users)
					for i in range(len(myresult)):
						callback += ";" + str(myresult[i][0])
					conn.send(callback.encode(FORMAT))
				else:
					conn.send("0;None".encode(FORMAT))
			
			#choose user
			elif code == "4":
				source, destination = msg.split(";",1)
				sql = "SELECT * FROM message WHERE (source = %s AND dest = %s) OR (source = %s AND dest = %s) ORDER BY id DESC"
				val = (source,destination,destination,source,)
				mycursor.execute(sql,val)
				myresult = mycursor.fetchall()
				if myresult is not None:
					callback = str(len(myresult))
					for i in range(len(myresult)):
						for j in range(4):
							callback += ";" + str(myresult[i][j])
					conn.send(callback.encode(FORMAT))
				else:
					conn.send("0;0".encode(FORMAT))
			elif code == "5":
				data = msg.split(";")
				sql = "INSERT INTO message (dest, source, text) VALUES(%s, %s, %s)"
				val = (data[2],data[1],data[0],)
				mycursor.execute(sql,val)
				mydb.commit()
				conn.send("1".encode(FORMAT))
			elif code == "6":
				if myUser != '':
					sql = "UPDATE users SET isLogged = 'No' WHERE username = %s"
					mycursor.execute(sql,(myUser,))
					mydb.commit()
				conn.send("1".encode(FORMAT))
	#loguot
	if myUser != '':
		sql = "UPDATE users SET isLogged = 'No' WHERE username = %s"
		mycursor.execute(sql,(myUser,))
		mydb.commit()
	myUser = ""
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