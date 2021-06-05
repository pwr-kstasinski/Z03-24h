import React, { useEffect, useState } from 'react';
import socketIOClient from "socket.io-client"

function getAllUsers() {
    return fetch("http://localhost:5000/users", { credentials: 'include' })
}

function UserList({ onUserSelect = (username) => { }, className }) {
    const [users, setUsers] = useState(null)
    const [selectedUsr, setSelectedUsr] = useState("")

    function getUserList() {
        getAllUsers()
            .then(response => response.json())
            .then(data => {
                if (data) {
                    console.log(data)
                    if (data.status == "succes") {
                        let users = []
                        users = data.users.sort((a, b) => {
                            // komparatory powinny być rozdzielone bo mamy niepotrzebną redundancje kodu
                            const dateA = new Date(a.recent_activity).getTime()
                            const dateB = new Date(b.recent_activity).getTime()
                            if (a.active && b.active) {
                                if (dateA > dateB)
                                    return -1

                                if (dateA < dateB)
                                    return 1

                                return 0
                            }
                            else if (!a.active && b.active)
                                return 1
                            else if (a.active && !b.active)
                                return -1
                            else {
                                if (dateA > dateB)
                                    return -1

                                if (dateA < dateB)
                                    return 1

                                return 0
                            }
                        })

                        setUsers(users)
                    }
                }
            })
    }

    useEffect(() => {
        getUserList()
        const socket = socketIOClient("http://127.0.0.1:5000")
        socket.on("reload_userlist", data => {
            if (data.who) {
                if (data.who == localStorage.getItem("username"))
                    getUserList()
            }
            else
                getUserList()
        })
    }, [])

    let users_comp = [(
        <button onClick={() => onUserSelect("")}>
            Global
        </button>
    )]

    if (users)
        users_comp.push(...users.map(user => {
            const style = { "display": "block" }
            if (!user.active)
                style["opacity"] = 0.5
            return (
                <button onClick={() => onUserSelect(user.name)} style={style}>
                    {user.name} - {user.new_messages_cont}
                </button>
            )
        }))



    return (
        <div className={className}>
            Użytkownicy:
            <ul>
                {users_comp}
            </ul>
        </div>
    )
}

export default UserList