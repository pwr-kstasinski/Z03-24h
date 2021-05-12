import React, { useEffect, useState } from 'react';

function getAllUsers() {
    return fetch("localhost:8000/users")
}

function UserList({ onUserSelect = (username) => { } }) {
    const [users, setUsers] = useState(null)
    const [selectedUsr, setSelectedUsr] = useState(null)

    useEffect(() => {
        getAllUsers()
            .then(response => response.json())
            .then(data => {
                if (data) {
                    if (data.status == "succes") {
                        setUsers(data.users)
                    }
                }
            })
    }, [])
}

export default UserList