from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from database import SessionLocal, Song
from pydantic import BaseModel

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Permitir solicitudes solo desde esta URL
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Model
class SongCreate(BaseModel):
    name: str
    artist: str
    album: str
    cover_url: str 

# Obtener una lista de canciones filtradas por artista
@app.get("/songs/")
async def get_songs(artist: str, db: Session = Depends(get_db)):
    songs = db.query(Song).filter(Song.artist == artist).all()
    # Incluir el nombre del artista en cada canción
    return [{"name": song.name, "artist": song.artist, "album": song.album, "cover_url": song.cover_url} for song in songs]


# Agregar una nueva canción
@app.post("/songs/")
async def add_song(song: SongCreate, db: Session = Depends(get_db)):
    new_song = Song(name=song.name, artist=song.artist, album=song.album, cover_url=song.cover_url)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return {"message": "Song added successfully", "song": new_song}

# Obtener una canción por ID
@app.get("/songs/{song_id}")
async def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

# Actualizar una canción
@app.put("/songs/{song_id}")
async def update_song(song_id: int, song: SongCreate, db: Session = Depends(get_db)):
    song_to_update = db.query(Song).filter(Song.id == song_id).first()
    if not song_to_update:
        raise HTTPException(status_code=404, detail="Song not found")
    
    song_to_update.name = song.name
    song_to_update.artist = song.artist
    song_to_update.album = song.album
    song_to_update.cover_url = song.cover_url

    db.commit()
    return {"message": "Song updated successfully", "song": song_to_update}

# Eliminar una canción
@app.delete("/songs/{song_id}")
async def delete_song(song_id: int, db: Session = Depends(get_db)):
    song_to_delete = db.query(Song).filter(Song.id == song_id).first()
    if not song_to_delete:
        raise HTTPException(status_code=404, detail="Song not found")
    
    db.delete(song_to_delete)
    db.commit()
    return {"message": "Song deleted successfully"}
