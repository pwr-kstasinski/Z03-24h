import React, { useEffect, useState } from 'react';
import UserList from './UserList';

function getMessagesFrom(username) {
    return fetch(`http://localhost:5000/recive/${username}`, { credentials: 'include' })
}

function getBrodcastMessages() {
    return fetch(`http://localhost:5000/brodcast`, { credentials: 'include' })
}

function sendMessage(username, content) {
    return fetch(`http://localhost:5000/brodcast`, {
        method: "POST",
        credentials: 'include',
        body: JSON.stringify({ content, username: "test" }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

function MsssageView({ username = "" }) {
    const [messages, setMessages] = useState(null)
    useEffect(() => {
        if (username == "") {
            getBrodcastMessages()
                .then(resp => resp.json())
                .then(data => {
                    console.log(data);
                    setMessages(data.messages)
                })
        }
        else {
            getMessagesFrom(username)
                .then(resp => resp.json())
                .then(data => {
                    setMessages(data.messages)
                })
        }
    }, [username])

    let message_comp = null
    console.log(messages);
    if (messages)
        message_comp = messages.map(mesage => {
            return (
                <li>
                    {mesage.content}
                </li>
            )
        })

    return (
        <div>
            {message_comp}
            <div>
                <input type="text"></input>
                <button>wyślij</button>
                <button>odśwież</button>
            </div>
        </div>
    )
}

export default MsssageView