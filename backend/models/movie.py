# Third Party
from sqlalchemy import Column, Integer, String

# Local
from config.database import Base


class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(String)
    category = Column(String)
