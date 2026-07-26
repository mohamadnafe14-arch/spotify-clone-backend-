import bcrypt
from fastapi import FastAPI, HTTPException
from database import db
import uuid
from models.base import Base
from models.user import User
from pydantic_schemas.user_create import UserCreate
app = FastAPI()
@app.post("/signUp")
def create_user(user: UserCreate):
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_db= User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db