# Paquetes externos
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import re

# Paquetes internos
from database import get_db
from model.note import Note
from model.user import User
from validate.note import *

api = FastAPI()

"""
Creación de notas y asignación a usuarios.
"""
@api.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
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
@api.get("/notes", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def listNotes(db: Session = Depends(get_db)):

    noteList = db.query(Note).all()
    return noteList

"""
Obtener el contenido de una nota.
"""
@api.get("/notes/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def listNotes(note_id, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found in database."
        )

    if len(note) > 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Persistance error."
        )
    
    return note

"""
Obtener notas que contengan una expresión.
"""
@api.get("/notes/searchExp?query={expression}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def searchNotesByExpression(expression, db: Session = Depends(get_db)):

    noteList = db.query(Note).filter(Note.content.ilike(f"%{expression}%")).all()

    if not noteList:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No notes contain: {expression}."
        )
    else:
        return noteList
    
"""
Obtener notas de un usuario.
"""
@api.get("/notes/searchUsr?query={userName}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def searchNotesByUser(userName, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.name == userName)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the name {userName}."
        )

    noteList = db.query(Note).filter(Note.user == userName).all()

    if not noteList:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {userName} doesn't have any notes."
        )
    else:
        return noteList
    
"""
Eliminar una nota.
"""
@api.delete("/notes", status_code=status.HTTP_202_ACCEPTED)
def deleteNote(note_id: NoteDelete, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id)
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found in database."
        )
    else:
        db.delete(note)
        db.commit()
