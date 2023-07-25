# FastAPI
from fastapi import status, Request, HTTPException
from fastapi.security import HTTPBearer

# Local
from jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'user@example.com':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials are invalid')
