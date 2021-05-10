from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status


class Message(BaseModel):
    text: str


app = FastAPI()

messagesDictionary = dict()

users = {
    "0": "",
    "1": "",
    "2": "",
    "3": "",
    "4": "",
    "5": ""
}


@app.put('/messages')
async def getMessages(messageTo: int, messageFrom: int, form_data: OAuth2PasswordRequestForm = Depends()):
    user = form_data.username
    if user not in users:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # print(messagesDictionary.get((messageTo, messageFrom), ["no messages"]))
    messagesList = messagesDictionary.get((messageTo, messageFrom))

    resultDict = {"empty": True, "messages": []}
    if messagesList is not None:
        resultDict["empty"] = False
        resultDict["messages"] = messagesList
        messagesDictionary[(messageTo, messageFrom)] = None

    return resultDict

"""
{
  "text": "string"
}
"""

@app.post('/messages')
async def sendMessage(messageTo: int, messageFrom: int, message: str, form_data: OAuth2PasswordRequestForm = Depends()):
    user = form_data.username
    if user not in users:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    data = message
    if messagesDictionary.get((messageTo, messageFrom)) is None:
        messagesDictionary[(messageTo, messageFrom)] = [data]
        # print(messagesDictionary[(messageTo, messageFrom)])
    else:
        updateList = messagesDictionary[(messageTo, messageFrom)]
        updateList.append(data)
        messagesDictionary[(messageTo, messageFrom)] = updateList
        # print(messagesDictionary[(messageTo, messageFrom)])

    return {"received": True}
