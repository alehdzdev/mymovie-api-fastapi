from typing import Annotated

# FastAPI
from fastapi import Path, Query, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Local
from config.database import SessionLocal
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import PostMovie


movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'])
async def get_movies(category: Annotated[str, Query(min_length=5, max_length=15)] = None):
    db = SessionLocal()
    return MovieService(db).get_movies(category)


@movie_router.get('/movies/{id}', tags=['movies'])
async def get_movie(id: int = Path(ge=1)):
    db = SessionLocal()
    movie = MovieService(db).get_movie(id)
    if movie:
        return movie
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)


@movie_router.post('/movies', tags=['movies'], dependencies=[Depends(JWTBearer())])
async def create_movie(movie: PostMovie) -> dict:
    db = SessionLocal()
    response = jsonable_encoder(MovieService(db).create_movie(movie))
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@movie_router.delete('/movies/{id}', tags=['movies'], status_code=204)
async def delete_movie(id: int):
    db = SessionLocal()
    result = MovieService(db).delete_movie(id)
    if result:
        return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)


@movie_router.put('/movies/{id}', tags=['movies'])
async def update_movie(id: int, movie: PostMovie):
    db = SessionLocal()
    result = MovieService(db).update_movie(id, movie)
    if result:
        return result
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)
