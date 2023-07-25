# FastAPI
from fastapi.encoders import jsonable_encoder

# Local
from models.movie import Movie as MovieModel
from schemas.movie import PostMovie


class MovieService():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self, category: str):
        if not category:
            return self.db.query(MovieModel).all()
        return self.db.query(MovieModel).filter(MovieModel.category.ilike(category)).all()

    def get_movie(self, id: int):
        return self.db.query(MovieModel).filter(MovieModel.id == id).first()

    def create_movie(self, data: PostMovie):
        movie = MovieModel(**data.dict())
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update_movie(self, id: int, data: PostMovie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if movie:
            if isinstance(data, dict):
                update_data = data
            else:
                update_data = data.dict(exclude_unset=True)
            for field in jsonable_encoder(movie):
                if field in update_data:
                    setattr(movie, field, update_data[field])
            self.db.add(movie)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        return None

    def delete_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if movie:
            self.db.delete(movie)
            self.db.commit()
            return True
        return None
