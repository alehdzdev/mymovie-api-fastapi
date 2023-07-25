# Third Party
from pydantic import BaseModel, Field


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
