import uuid
import traceback
import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from database import get_db
from middleware.auth_middleware import auth_middleware
from models.favourite import Favourite
from models.song import Song
from pydantic_schemas.favourite_song import FavouriteSong
from dotenv import load_dotenv
import os
import cloudinary

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)
router = APIRouter()

@router.post("/upload",status_code = 201)
async def upload(song: UploadFile = File(...)
                 ,thumbnail: UploadFile = File(...)
                 ,artist: str = Form(...)
                 ,songName: str = Form(...)
                 ,color_hex: str = Form(...)
                 ,auth_info: dict = Depends(auth_middleware)
                 , db: Session = Depends(get_db)):
    try:
        song_id = str(uuid.uuid4())
        thumbnail_response = cloudinary.uploader.upload(thumbnail.file,
                                                        resource_type="image",
                                                    folder=f"songs/{song_id}")
        song_response = cloudinary.uploader.upload(song.file,
                                                resource_type="auto",
                                                folder=f"songs/{song_id}")
        song = Song(id=song_id,
                    song_name=songName,
                    artist=artist,
                    color_hex=color_hex,
                    thumbnail_url=thumbnail_response["secure_url"],
                    song_url=song_response["secure_url"])
        db.add(song)
        db.commit()
        db.refresh(song)
        return {"song": song}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/")
def get_songs(db: Session = Depends(get_db), auth_info: dict = Depends(auth_middleware)):
    songs = db.query(Song).all()
    return songs
@router.post("/favourite")
def toggle_favourite(favourite_song: FavouriteSong
                  ,db:Session = Depends(get_db)
                  , auth_info: dict = Depends(auth_middleware)
                  ):
    try:
        user_id = auth_info["id"]
        song_id = favourite_song.id
        favourite = db.query(Favourite).filter(Favourite.user_id == user_id, Favourite.song_id == song_id).first()
        if favourite:
            db.delete(favourite)
            db.commit()
            return {"message": "Removed"}
        else:
            new_favourite = Favourite(id=str(uuid.uuid4()), user_id=user_id, song_id=song_id)
            db.add(new_favourite)
            db.commit()
            db.refresh(new_favourite)
            return {"message": "Added"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/favourites")    
def get_favourites(db: Session = Depends(get_db), auth_info: dict = Depends(auth_middleware)):
    try:
        user_id = auth_info["id"]
        favourites = db.query(Favourite).filter(Favourite.user_id == user_id).options(joinedload(Favourite.song)).all()
        return favourites
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))