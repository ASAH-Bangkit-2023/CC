from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder

from jose import jwt
from pydantic import ValidationError

from .utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from schemas.token import TokenPayLoad
from schemas.user import UserOut
from config.db import engine
from models import asah_models
from db_crud.user import getUser
from sqlalchemy.orm import Session
from config.db import get_db

asah_models.Base.metadata.create_all(bind=engine)

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

async def get_current_user(token: str = Depends(reusable_oauth), db: Session = Depends(get_db)) -> UserOut:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_data = TokenPayLoad(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    fetch_user = jsonable_encoder(getUser(db, token_data.sub))
    if fetch_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserOut(**fetch_user)