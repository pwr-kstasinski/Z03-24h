import React, { useEffect, useState } from 'react';

function getAllUsers() {
    return fetch("http://localhost:5000/users", { credentials: 'include' })
}

function UserList({ onUserSelect = (username) => { } }) {
    const [users, setUsers] = useState(null)
    const [selectedUsr, setSelectedUsr] = useState(null)

    useEffect(() => {
        getAllUsers()
            .then(response => response.json())
            .then(data => {
                if (data) {
                    console.log(data)
                    if (data.status == "succes") {
                        setUsers(data.users)
                    }
                }
            })
    }, [])

    let users_comp = null
    if (users)
        users_comp = users.map(user => {
            return (
                <li>
                    {user.name}
                </li>
            )
        })

    return (
        <div>
            {users_comp}
        </div>
    )
}

export default UserList