from sqlalchemy import TEXT, VARCHAR, Column
from models.base import Base
class Song(Base):
    __tablename__ = "songs"
    id = Column(TEXT, primary_key=True)
    song_name = Column(VARCHAR(100))
    artists = Column(VARCHAR(100))
    color_hex = Column(VARCHAR(6))
    thumbnail_url = Column(VARCHAR(100))
    song_url = Column(VARCHAR(100))