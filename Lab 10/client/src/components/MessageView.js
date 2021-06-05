import React, { useEffect, useState, useRef } from 'react';
import socketIOClient from "socket.io-client"

import Message from "./Message"
import "./MessageView.css"

function getMessagesFrom(username) {
    if (username == "")
        return fetch(`http://localhost:5000/brodcast`, { credentials: 'include' })
    return fetch(`http://localhost:5000/recive/${username}`, { credentials: 'include' })
}

function markAsReaded(msg_ids) {
    return fetch(`http://localhost:5000/readed`, {
        method: "POST",
        credentials: 'include',
        body: JSON.stringify({ msg_ids }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

function sendMessage(username, content) {
    if (username == "")
        return fetch(`http://localhost:5000/brodcast`, {
            method: "POST",
            credentials: 'include',
            body: JSON.stringify({ content }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
    return fetch(`http://localhost:5000/send`, {
        method: "POST",
        credentials: 'include',
        body: JSON.stringify({ content, target: username }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
}


function MsssageView({ username = "", llogedUsername = "", className }) {
    const [messages, setMessages] = useState(null)
    const messageRef = useRef(null)

    const markAllAsReaded = () => {
        if (!messages)
            return

        const msg_ids = messages.filter(msg => !msg.readed).map(msg => msg.id)
        markAsReaded(msg_ids)
    }

    function handleMessageRefresh() {
        getMessagesFrom(username)
            .then(resp => resp.json())
            .then(data => {
                setMessages(data.messages)
                markAllAsReaded()
            })
    }

    const handleMessageSend = () => {
        const content = messageRef.current.value
        sendMessage(username, content)
            .then(resp => resp.json())
            .then(data => {
                console.log(data);
                handleMessageRefresh()
            })
        messageRef.current.value = ""
    }

    function onMessageReload(data) {
        if (!data.who)
            handleMessageRefresh()

        if (data.who == llogedUsername && data.from == username)
            handleMessageRefresh()
    }

    useEffect(() => {
        handleMessageRefresh()
        const socket = socketIOClient("http://127.0.0.1:5000")
        socket.on("reload_messages", onMessageReload)
    }, [username])

    let message_comp = null
    console.log(messages);
    if (messages)
        message_comp = messages.map(mesage => {
            return (
                <Message
                    content={mesage.content}
                    sender={mesage.sender}
                    readed={mesage.readed}
                    time={mesage.time}
                />
            )
        })

    return (
        <div className={className}>
            <h2>Wiadomości od {username || "Wszystkich"}</h2>
            <div className="message-container">
                {message_comp}
            </div>
            <div className="message-container_send">
                <input type="text" ref={messageRef}
                    className="message-container_send-inp"></input>
                <button
                    className="message-container_send-btn"
                    onClick={handleMessageSend}>wyślij</button>
                {/* <button onClick={handleMessageRefresh}>odśwież</button> */}
            </div>
        </div>
    )
}

export default MsssageView