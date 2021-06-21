import React, { useRef } from 'react';

function RejestracjaU({ onRegister = (usr_name,room_name) => { } }) {
    const refUsr = useRef()
    const refIDP = useRef()

    return (
        <div>
            <input type="text" placeholder="Nazwa urzytkownika" ref={refUsr}></input>
            <input type="text" placeholder="ID pokoju" ref={refIDP}></input>
            <button onClick={() => onRegister(refUsr.current.value, refIDP.current.value)}>Zarejestruj użytkownika w pokoju</button>
        </div>
    )
}

export default RejestracjaU