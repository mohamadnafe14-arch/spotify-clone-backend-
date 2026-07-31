import uuid
import traceback
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