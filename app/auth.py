from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserSchema
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from app.database import get_db
from app.models import User

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@auth_router.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = Authorize.create_access_token(subject=user.email)
    return {"access_token": access_token}
