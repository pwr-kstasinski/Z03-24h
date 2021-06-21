import React from 'react'
import "./Message.css"

export default function Message({ content = "", readed = true, sender = "", time = "" }) {
    const msg_classes = "message" + (sender == localStorage.getItem("username") ? " message--own" : "") +
        (readed ? "" : " message--notReaded")
    sender = (sender == localStorage.getItem("username") ? "Ja" : sender)
    return (
        <div className={msg_classes}>
            <div className="message__time">{time}</div>
            <div className="message__sender">{sender}</div>
            <div className="message__content">{content}</div>
            <div className="message__status">{readed}</div>
        </div>
    )
}