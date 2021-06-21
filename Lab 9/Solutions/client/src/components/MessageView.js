import React, { useEffect, useState, useRef } from 'react';

function getMessagesFrom(username) {
    if (username == "")
        return fetch(`http://localhost:5000/brodcast`, { credentials: 'include' })
    return fetch(`http://localhost:5000/recive/${username}`, { credentials: 'include' })
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

function MsssageView({ username = "", llogedUsername = "" }) {
    const [messages, setMessages] = useState(null)
    const messageRef = useRef(null)

    useEffect(() => {
        handleMessageRefresh()
    }, [username])

    const handleMessageRefresh = () => {
        getMessagesFrom(username)
            .then(resp => resp.json())
            .then(data => {
                setMessages(data.messages)
            })
    }

    const handleMessageSend = () => {
        const content = messageRef.current.value
        sendMessage(username, content)
            .then(resp => resp.json())
            .then(data => {
                console.log(data);
            })
    }

    let message_comp = null
    console.log(messages);
    if (messages)
        message_comp = messages.map(mesage => {
            return (
                <li>
                    <b>{mesage.sender}</b>: {mesage.content}
                </li>
            )
        })

    return (
        <div>
            <h2>Wiadomości od {username || "Wszystkich"}</h2>
            {message_comp}
            <div>
                <input type="text" ref={messageRef}></input>
                <button onClick={handleMessageSend}>wyślij</button>
                <button onClick={handleMessageRefresh}>odśwież</button>
            </div>
        </div>
    )
}

export default MsssageView