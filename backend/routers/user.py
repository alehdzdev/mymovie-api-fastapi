# FastAPI
from fastapi import APIRouter

# Local
from jwt_manager import create_token
from schemas.user import User


user_router = APIRouter()


@user_router.post('/login', tags=['auth'])
async def login(user: User):
    if user.email == "user@example.com" and user.password == "string":
        token: str = create_token(user.dict())
        return {token}
