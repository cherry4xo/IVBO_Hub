import logging
import hmac
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import jwt
from fastapi import HTTPException, Security, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
# from jwt import PyJWTError
# from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_403_FORBIDDEN

from app.applications.users.models import User
from app.core.auth.schemas import JWTTokenPayload, TelegramLoginData
from app.core.auth.utils import password
from app.core.auth.utils.jwt import ALGORITHM
from app.settings.config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)) -> Optional[User]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = JWTTokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    
    user = await User.filter(uuid=token_data.user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


async def get_current_admin(current_user: User = Security(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="The user does not have enough privileges")
    
    return current_user


def validate(data: TelegramLoginData, secret_key: str) -> bool:
    telegram_data = data.dict(
        exclude_unset=True,
        exclude_none=True,
        exclude_defaults=True
    )
    data_check_string = '\n'.join(sorted([
        f"{key}={value or 'null'}"
        for key, value in telegram_data.items()
        if key != 'hash' and value is not None
    ]))
    secret_key = hashlib.sha256(secret_key.encode()).digest()
    calculated_hash = hmac.new(
        secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    return data.hash == calculated_hash


async def authenticate(credentials: TelegramLoginData) -> Optional[User]:
    if credentials.username:
        user = await User.get_by_tg_username(username=credentials.username)
    else:
        return None

    if user is None:
        user = await User.create(credentials)

    verified = validate(credentials, settings.BOT_TOKEN)

    if verified:
        return user
    return None