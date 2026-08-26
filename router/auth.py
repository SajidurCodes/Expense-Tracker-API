from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from typing import Annotated
from database import SessionLocal
from models import Users
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
import os
from dotenv import load_dotenv






load_dotenv()



router = APIRouter()


bcrypt_context =CryptContext(schemes=['bcrypt'], deprecated='auto')
OAuth2_bearer =OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')



if SECRET_KEY is None:
    raise ValueError('SECRET_KEY is not set')


class CreateUsers(BaseModel):


    email: str
    username: str
    password: str


def authenticate_user(username, password, db):


    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        return False

    if bcrypt_context.verify(password, user.hash_password):
        return user

    return False


def create_access_token(username: str, user_id: int, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})


    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')


        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail='User not found')
        return {'username': username, 'id': user_id}
    

    except:

        raise HTTPException(status_code=401, detail='Failed Authentication')


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/auth/register')
def create_users(db: db_dependency, new_user: CreateUsers):

    existing_user = db.query(Users).filter(Users.username == new_user.username).first()

    if existing_user is not None:
        raise HTTPException(status_code=400, detail='Username already exists')

    existing_email = db.query(Users).filter(Users.email == new_user.email).first()

    if existing_email is not None:
        raise HTTPException(status_code=400, detail='Email already exists')

    user_model = Users(
        email=new_user.email,
        username=new_user.username,
        hash_password=bcrypt_context.hash(new_user.password),
    )

    db.add(user_model)
    db.commit()

    return JSONResponse(
        status_code=201,
        content={'message': 'User created successfully!!!!!'}
    )


@router.post('/auth/login')
def login_user(db: db_dependency,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    token = create_access_token(
        user.username,
        user.id,
        timedelta(minutes=30)
    )

    return {
        'access_token': token,
        'token_type': 'bearer'
    }