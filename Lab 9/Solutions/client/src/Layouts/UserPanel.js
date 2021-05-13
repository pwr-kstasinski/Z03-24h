import React from 'react';
import UserList from '../components/UserList'

function UserPanel({ username }) {
    return (
        <div>
            Witaj {username}
            <UserList></UserList>
        </div>
    )
}

export default UserPanel