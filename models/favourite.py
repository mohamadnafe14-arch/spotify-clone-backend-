from sqlalchemy import TEXT, Column
from models.base import Base
class Favourite(Base):
    __tablename__ = "favourites"
    id = Column(TEXT, primary_key=True)
    user_id = Column(TEXT)
    song_id = Column(TEXT)