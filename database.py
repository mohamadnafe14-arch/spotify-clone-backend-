from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "postgresql://postgres:medo2005#@localhost:5432/spotify"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()