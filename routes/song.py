import uuid

import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from database import get_db
from middleware.auth_middleware import auth_middleware
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
        folder_name = str(uuid.uuid4())
        thumbnail_url = cloudinary.uploader.upload(fileobj=thumbnail.file,
                                                    folder=f"songs/{folder_name}")
        song_url = cloudinary.uploader.upload(fileobj=song.file,
                                                folder=f"songs/{folder_name}")
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))