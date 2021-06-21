import React, { useState } from 'react';
import UserList from '../components/UserList'
import MessageView from '../components/MessageView'

function UserPanel({ username, onLogout = () => { } }) {
    const [selectedUser, setSelectedUser] = useState("")

    const handleUserSelect = (username) => {
        setSelectedUser(username)
    }

    return (
        <div>
            Witaj {username} <button onClick={onLogout}>Wyloguj</button>
            <hr></hr>
            <UserList onUserSelect={handleUserSelect}></UserList>
            <hr />
            <MessageView username={selectedUser} llogedUsername={username}></MessageView>
        </div>
    )
}

export default UserPanel