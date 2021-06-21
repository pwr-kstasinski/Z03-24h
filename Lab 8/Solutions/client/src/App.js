import React, { useState, useRef } from 'react';
import RejestracjaU from './Components/RejestracjaU'
import Wiadomosci from './Components/Wiadomosci'

function joinRoom(room_id, user_name) {
  return fetch(`http://127.0.0.1:8000/join/${room_id}/${user_name}`, {
    method: "PUT"
  })
}

function getMessages(room_id, user_name) {
  return fetch(`http://127.0.0.1:8000/room/${room_id}/${user_name}`, { method: "GET" })
}

function createRoom(room_id) {
  return fetch(`http://127.0.0.1:8000/room/${room_id}`, { method: "PUT" })
}

function sendMessage(room_id, { sender, message }) {
  return fetch(`http://127.0.0.1:8000/room/${room_id}`, {
    method: "POST",
    body: JSON.stringify({ sender, message })
  })
}

function App() {
  const [userName, setUserName] = useState(null)
  const [roomID, setRoomID] = useState(null)
  const [logInMSG, setLogInMSG] = useState(null)
  const [roomMSG, setRoomMSG] = useState(null)
  const [messages, setMessages] = useState([])
  const roomRef = useRef()


  const handleRegister = (usr_name, room_id) => {
    joinRoom(room_id, usr_name)
      .then(response => {
        if (response.ok)
          return response.json()
      }).then(data => {
        if (data[0].status == "succes") {
          console.log(data);
          setUserName(usr_name)
          setRoomID(room_id)
          setLogInMSG(data[0].message)
        }
        else if (data[0].status == "fail") {
          setLogInMSG(data[0].couse)
        }
      })
  }

  const handleRefresh = () => {
    if (!userName || !roomID)
      return
    getMessages(roomID, userName)
      .then(response => {
        if (response.ok)
          return response.json()
      }).then(data => {
        setMessages(prev => [...prev, ...data[0].messages])
      })
  }

  const handleCreateRoom = roomID => {
    createRoom(roomID)
      .then(response => {
        if (response.ok)
          return response.json()
      }).then(data => {
        console.log(data);
        if (data[1] == "200" || data[1] == "201")
          setRoomMSG(data[0].message)
        else
          setRoomMSG(data[0].couse)
      })
  }

  const handleMSGSend = msg => {
    if (!userName || !roomID)
      return
    sendMessage(roomID, { sender: userName, message: msg })
      .then(response => {
        return response.json()
      }).then(data => {
        if (data[0].status == "succes")
          setMessages(prev => [...prev, { content: msg, from: "Me" }])
      })
  }


  return (
    <div className="App">
      <div>
        <input type="text" placeholder="ID nowego pokoju" ref={roomRef}></input>
        <button onClick={() => handleCreateRoom(roomRef.current.value)}>Zarejestruj pokój</button> {roomMSG}
      </div>
      {!!userName || <RejestracjaU onRegister={handleRegister} />}
      <h1>{logInMSG}</h1>
      {(userName && roomID) && <Wiadomosci messages={messages} onRefresh={handleRefresh} onSend={handleMSGSend} />}
    </div >
  );
}

export default App;
