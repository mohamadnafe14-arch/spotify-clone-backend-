import uuid

import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from database import get_db
from middleware.auth_middleware import auth_middleware
from models.song import Song
cloudinary.config( 
    cloud_name = "ebia0lc9", 
    api_key = "414348853487241", 
    api_secret = "UJeZw8N8n4QEwBXFID95evYn7GU", 
    secure=True
)
router = APIRouter()

@router.post("/upload")
async def upload(song: UploadFile = File(...)
                 ,thumbnail: UploadFile = File(...)
                 ,artists: str = Form(...)
                 ,songName: str = Form(...)
                 ,color_hex: str = Form(...)
                 ,auth_info: dict = Depends(auth_middleware)
                 , db: Session = Depends(get_db)):
    try:
        song_id = str(uuid.uuid4())
        thumbnail_response = cloudinary.uploader.upload(fileobj=thumbnail.file,
                                                    folder=f"songs/{song_id}")
        song_response = cloudinary.uploader.upload(fileobj=song.file,
                                                folder=f"songs/{song_id}")
        song = Song(id=song_id,
                    song_name=songName,
                    artists=artists,
                    color_hex=color_hex,
                    thumbnail_url=thumbnail_response["url"],
                    song_url=song_response["url"])
        db.add(song)
        db.commit()
        db.refresh(song)
        return {"song": song}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))