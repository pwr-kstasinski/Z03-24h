import React, { useState } from 'react';
import UserList from '../components/UserList'
import MessageView from '../components/MessageView'

function UserPanel({ username }) {
    const [selectedUser, setSelectedUser] = useState("")
    const handleUserSelect = (username) => {
        setSelectedUser(username)
        alert(username)
    }

    return (
        <div>
            Witaj {username}
            <UserList onUserSelect={handleUserSelect}></UserList>
            <hr />
            <MessageView username={selectedUser}></MessageView>
        </div>
    )
}

export default UserPanel