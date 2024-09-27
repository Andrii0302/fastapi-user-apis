from fastapi import FastAPI,Depends, HTTPException,Path,APIRouter
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
import models
from .auth import get_current_user
from passlib.context import CryptContext
router=APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(models.Users).filter(models.Users.id == user.get('id')).first()

@router.put('/change-password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,user_request:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)
    db.add(user_model)
    db.commit()

@router.put('/change-phone/{phone_number}',status_code=status.HTTP_204_NO_CONTENT)
async def change_phone(user:user_dependency,db:db_dependency,phone_number:str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()