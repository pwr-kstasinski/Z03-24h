from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

import crud
import database_models
import schemas
from database import SessionLocal, engine

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=int(token))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nickname(db, nick=user.nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/active_users/", response_model=List[schemas.UserActive])
def read_active_users(db: Session = Depends(get_db),
                      current_user: schemas.User = Depends(get_user_from_token)):
    users = crud.get_active_users(db=db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = crud.get_user_by_nickname(db, nick=form_data.username)
    if user_dict is None:
        raise HTTPException(status_code=400, detail="Incorrect username")
    password = user_dict.hashed_password
    if not password == form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"access_token": user_dict.id, "token_type": "bearer"}


@app.post("/messages/{messageTo}/", response_model=schemas.Message)
def post_message(
        messageTo: str, message: schemas.MessageCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_user_from_token)
):
    current_user_id = current_user.id

    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    db_recipient = crud.get_user_by_nickname(db, nick=messageTo)
    if db_recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return crud.create_message(db=db, message=message, recipient_id=db_recipient.id, sender_id=current_user_id)


@app.get("/messages/{messageFrom}", response_model=List[schemas.Message])
def get_messages(messageFrom: str,
                 db: Session = Depends(get_db),
                 current_user: schemas.User = Depends(get_user_from_token)):
    current_user_id = current_user.id

    crud.update_last_activity_of_user(db=db, user_id=current_user_id)

    db_sender = crud.get_user_by_nickname(db, nick=messageFrom)
    if db_sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")
    messages = crud.get_messages_by_users_id(db, sender_id=db_sender.id, recipient_id=current_user_id)
    return messages


@app.get("/items/", response_model=List[schemas.Message])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_messages(db, skip=skip, limit=limit)
    return items


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
