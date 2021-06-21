import React, { useEffect, useState } from 'react';

function getAllUsers() {
    return fetch("http://localhost:5000/users", { credentials: 'include' })
}

function UserList({ onUserSelect = (username) => { } }) {
    const [users, setUsers] = useState(null)
    const [selectedUsr, setSelectedUsr] = useState("")

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

    let users_comp = [(
        <button onClick={() => onUserSelect("")}>
            Global
        </button>
    )]

    if (users)
        users_comp.push(...users.map(user => {
            return (
                <button onClick={() => onUserSelect(user.name)} style={{ "display": "block" }}>
                    {user.name}
                </button>
            )
        }))



    return (
        <div>
            Użytkownicy:
            <ul>
                {users_comp}
            </ul>
        </div>
    )
}

export default UserList