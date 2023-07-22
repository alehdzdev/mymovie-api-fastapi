from typing import Annotated

# FastAPI
from fastapi import FastAPI, Path, Query, status, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

# Third Party
from pydantic import BaseModel, Field, EmailStr

# Local
from jwt_manager import create_token, validate_token
from config.database import SessionLocal
from models.movie import Movie as MovieModel


app = FastAPI()
app.title = 'MyMovie API'
app.version = '0.0.1'


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'user@example.com':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credentials are invalid')


class User(BaseModel):
    email: EmailStr
    password: str


class PostMovie(BaseModel):
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)


class Movie(PostMovie):
    id: int

    class Config:
        from_attributes = True


@app.get('/')
async def hello_world():
    return HTMLResponse('<h1>Hello World!</h1>')


@app.post('/login', tags=['auth'])
async def login(user: User):
    if user.email == "user@example.com" and user.password == "string":
        token: str = create_token(user.dict())
        return {token}


@app.get('/movies', tags=['movies'])
async def get_movies(category: Annotated[str, Query(min_length=5, max_length=15)] = None):
    db = SessionLocal()
    if not category:
        result = db.query(MovieModel).all()
        return result

    result = db.query(MovieModel).filter(MovieModel.category.ilike(category)).all()
    return result


@app.get('/movies/{id}', tags=['movies'])
async def get_movie(id: int = Path(ge=1)):
    db = SessionLocal()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if movie:
        return movie
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)


@app.post('/movies', tags=['movies'], dependencies=[Depends(JWTBearer())])
async def create_movie(movie: PostMovie) -> dict:
    db = SessionLocal()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={'message': 'The movie created successfully.'})


@app.delete('/movies/{id}', tags=['movies'], status_code=204)
async def delete_movie(id: int):
    db = SessionLocal()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        db.delete(result)
        db.commit()
        return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)


@app.put('/movies/{id}', tags=['movies'])
async def update_movie(id: int, movie: PostMovie):
    db = SessionLocal()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit()
        return movie
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
