from typing import Annotated, Dict

# Third Party
from fastapi import FastAPI, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

# Local
# from jwt_manager import create_token


app = FastAPI()
app.title = 'MyMovie API'
app.version = '0.0.1'


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)


class PostMovie(Movie):
    id: int


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Aventura'
    },
    {
        'id': 2,
        'title': 'Rambo',
        'overview': "Pum pum pu,",
        'year': '1982',
        'rating': 8,
        'category': 'Acción'
    }
]


@app.get('/')
async def hello_world():
    return HTMLResponse('<h1>Hello World!</h1>')


@app.post('/login', tags=['auth'])
async def login(user: User):
    return user


@app.get('/movies', tags=['movies'])
async def get_movies(category: Annotated[str, Query(min_length=5, max_length=15)] = None):
    if not category:
        return JSONResponse(content=movies)
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=data)


@app.get('/movies/{id}', tags=['movies'])
async def get_movie(id: int = Path(ge=1)):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return JSONResponse(content={}, status_code=status.HTTP_404_NOT_FOUND)


@app.post('/movies', tags=['movies'])
async def create_movie(movie: PostMovie) -> Dict:
    movies.append(movie)
    return JSONResponse(content={'message': 'The movie created successfully.'})


@app.delete('/movies/{id}', tags=['movies'], status_code=204)
async def delete_movie(id: int):
    for i in range(len(movies)):
        if movies[i]['id'] == id:
            del movies[i]
            break


@app.put('/movies/{id}', tags=['movies'])
async def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
        return item
    return []
