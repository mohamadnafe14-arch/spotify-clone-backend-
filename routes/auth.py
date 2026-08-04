import uuid
from sqlalchemy.orm import Session, joinedload
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from middleware.auth_middleware import auth_middleware
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
import jwt
router = APIRouter()
@router.post("/signUp",status_code=201)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
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
    token = jwt.encode({"id": user_db.id}, "secret")
    return {"token": token, "user": user_db}
@router.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).options(joinedload(User.favourites)).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="User does not exist")
    if not bcrypt.checkpw(user.password.encode(), user_db.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = jwt.encode({"id": user_db.id}, "secret")    
    return {"token": token, "user": user_db}
@router.get("/")
def get_current_users(db:Session=Depends(get_db),user_info:dict=Depends(auth_middleware)):
    user_db = db.query(User).filter(User.id == user_info["id"]).options(joinedload(User.favourites)).first()
    if not user_db:
        raise HTTPException(404,"User not found")
    return {"user": user_db, "token": user_info["x_auth_token"]}