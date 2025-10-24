# Paquetes externos
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

# Paquetes internos
from database import get_db
from model.note import Note
from model.user import User
from validate.note import *

router = APIRouter(prefix="/notes", tags=["Notes"])

"""
Creación de notas y asignación a usuarios.
"""
@router.post("", response_model=NoteCreate, status_code=status.HTTP_201_CREATED)
def createNote(note: NoteCreate, db: Session = Depends(get_db)):

    # Comprobación de usuario
    owner = db.query(User).filter(User.id == note.user_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {note.user_id} not found."
        )

    # Creación de la nueva nota validando con "NoteCreate"
    newNote = Note(
        title=note.title,
        file_path=note.file_path,
        user_id=note.user_id,
    )

    # Leer contenido del archivo y añadirlo content
    try:
        with open(note.file_path, "r", encoding="utf-8") as f:
            newNote.content = f.read()
            print(newNote.content)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File not found at the given path."
        )

    # Persistencia en SQLite
    db.add(newNote)
    db.commit()
    db.refresh(newNote)

    return newNote

"""
Listar todas las notas.
"""
@router.get("", response_model=List[NoteResponse], status_code=status.HTTP_200_OK)
def listNotes(db: Session = Depends(get_db)):

    noteList = db.query(Note).all()
    return noteList

"""
Obtener el contenido de una nota.
"""
@router.get("/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def getNote(note_id, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found in database."
        )
    
    return note

"""
Eliminar una nota.
"""
@router.delete("/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def deleteNote(note_id: int, db: Session = Depends(get_db)):
    
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        raise HTTPException(status_code=404,
                            detail="Note not found."
                            )
    
    db.delete(note)
    db.commit()

    return {"message": f"Nota {note_id} borrada correctamente."}