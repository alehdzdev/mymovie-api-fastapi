# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Local
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router


app = FastAPI()
app.title = 'MyMovie API'
app.version = '0.0.1'
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)


@app.get('/')
async def hello_world():
    return HTMLResponse('<h1>Hello World!</h1>')
