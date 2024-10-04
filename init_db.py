from database import SessionLocal, Song

# Inicializar la base de datos con datos de ejemplo
def init_db():
    db = SessionLocal()
    songs = [
        Song(name="Rolling in the Deep", artist="Adele", album="21", preview_url="http://example.com/song1"),
        Song(name="Someone Like You", artist="Adele", album="21", preview_url="http://example.com/song2"),
        Song(name="Shape of You", artist="Ed Sheeran", album="Divide", preview_url="http://example.com/song3"),
        Song(name="Blinding Lights", artist="The Weeknd", album="After Hours", preview_url="http://example.com/song4"),
    ]
    
    # Agregar las canciones a la base de datos
    db.add_all(songs)
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
