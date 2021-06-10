import React, { useState } from 'react';
import UserList from '../components/UserList'
import MessageView from '../components/MessageView'

import "./UserPanel.css"

function UserPanel({ username, onLogout = () => { } }) {
    const [selectedUser, setSelectedUser] = useState("")

    const handleUserSelect = (username) => {
        setSelectedUser(username)
    }

    return (
        <div className="user-panel">
            <h3 className="user-panel__header">Witaj {username} <button onClick={onLogout}>Wyloguj</button></h3>
            <hr></hr>
            <UserList className="user-panel__user-list" onUserSelect={handleUserSelect}></UserList>
            <hr />
            <MessageView className="user-panel__message-view" username={selectedUser} llogedUsername={username}></MessageView>
        </div>
    )
}

export default UserPanel