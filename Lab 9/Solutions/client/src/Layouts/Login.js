import React, { useRef } from 'react';

function login(username, password) {
    return fetch('http://localhost:5000/login', {
        method: 'POST',
        body: JSON.stringify({ usr_name: username, passwd: password })
    })
}

function Login({ onLoginSucces = (username, loginMessage) => { } }) {
    const passRef = useRef()
    const loginRef = useRef()

    const handleLogin = () => {
        const username = loginRef.current.value
        const password = passRef.current.value

        login(username, password)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data) {
                    if (data.status == "succes") {
                        alert("YEEE")
                        onLoginSucces(username, "")
                    }
                }
            })
    }

    return (
        <div className="login">
            <input type="text" ref={loginRef}></input>
            <input type="text" ref={passRef}></input>
            <button onClick={handleLogin}>Zaloguj</button>
            <button>Zarejestruj</button>
        </div>
    )

}

export default Login