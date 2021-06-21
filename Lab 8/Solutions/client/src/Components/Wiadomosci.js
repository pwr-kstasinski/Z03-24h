import React, { useRef } from 'react';

function Wiadomosci({ onSend = (msg) => { }, onRefresh = () => { }, messages = [] }) {
    const msgRef = useRef()

    const wiadomosci = messages.map(msg => {
        return (
            <li>
                
                <b>{msg.from}: </b>{msg.content}
            </li>
        )
    })
    return (
        <div>
            <h2>Wiadomości:</h2>
            <div>
                {wiadomosci}
            </div>
            <input type="text" placeholder="wiadomość..." ref={msgRef}></input>
            <button onClick={() => onSend(msgRef.current.value)}>Wyślij</button>
            <button onClick={() => onRefresh()}>Odśwież</button>
        </div>
    )
}

export default Wiadomosci