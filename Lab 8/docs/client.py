from tkinter import END
from openapi_client.api.sending_messages_api import SendingMessagesApi
from openapi_client.api.receiving_messages_api import ReceivingMessagesApi
from openapi_client import Configuration, ApiClient, ApiException
import tkinter as tk
from pprint import pprint

configuration = Configuration(
    host="http://127.0.0.1:5000"
)

username = ""
message_text = ""


def getMessages():
    with ApiClient(configuration) as api_client:
        api_instance = ReceivingMessagesApi(api_client)
        try:
            api_response = api_instance.get_username_get(username)
            response = api_response.to_dict()
            pprint(api_response)
            received_msg.insert(END, " -> " + username + ": ")
            for message in response['messages']:
                received_msg.insert(END, message)

        except ApiException as e:
            print("Exception when calling MessageApi->get_username_get: %s\n" % e)


def sendMessage():
    with ApiClient() as api_client:
        api_instance = SendingMessagesApi(api_client)
        receiver_username = dest_entry.get()
        message_text = messagebox.get("1.0", END)

        try:
            api_instance.send_receiver_username_message_post(receiver_username, message_text)
            received_msg.insert(END, username + " -> " + receiver_username + ": " + message_text)
        except ApiException as e:
            print("Exception when calling MessageApi->send_receiver_username_message_post: %s\n" % e)


def loginDraw(root):
    username_lbl = tk.Label(root, text='Podaj swoją nazwę:')
    global username_entry
    username_entry = tk.Entry(root)
    btn = tk.Button(root, text="Enter", command=lambda: chatViewDraw(root))
    username_lbl.pack()
    username_entry.pack()
    btn.pack()


def chatViewDraw(root):
    global username
    username = username_entry.get()
    for elem in root.winfo_children():
        elem.destroy()
    logged_lbl = tk.Label(root, text="Zalogowany jako: " + username)
    logged_lbl.grid(row=0, column=0)
    global received_msg
    received_msg = tk.Text(root, height=10, width=60)
    received_msg.grid(row=1, columnspan=8)
    dest_lbl = tk.Label(root, text="Odbiorca: ")
    dest_lbl.grid(row=5, column=0)
    global dest_entry
    dest_entry = tk.Entry(root)
    dest_entry.grid(row=5, column=1)
    global messagebox
    messagebox = tk.Text(root, height=6, width=60)
    messagebox.grid(row=6, columnspan=8)
    btn_getMessages = tk.Button(root, text="Pobierz", command=getMessages)
    btn_getMessages.grid(row=7, column=0)
    btn_sendMessage = tk.Button(root, text="Wyślij", command=sendMessage)
    btn_sendMessage.grid(row=7, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chatapp")
    root.geometry("480x350")
    loginDraw(root)
    root.mainloop()
