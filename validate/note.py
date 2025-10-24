"""
Clase: 
    Note
Tipo:
    Schema pydantic
Descripción:
    Esta clase define las validaciones pydantic de las entradas y salidas de la clase Note.
"""
import re
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

# Validador del modelo base
class NoteBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=30, description="Título de la nota (mínimo 5 caracteres y máximo 30)")

# Validador para el endpoint de creación de notas
class NoteCreate(NoteBase):
    file_path: str = Field(..., description="Ruta local del archivo .txt o .md")
    user_id: int

    @field_validator("file_path")
    def correctFileExtension(cls, value):
        regex = r".*\.(md|txt)$"
        correctFileExtension = re.match(regex, value)
        if correctFileExtension:
            return value
        else:
            raise ValueError("You must upload a .md or .txt file")

# Validador para el endpoint de muestra de notas
class NoteResponse(NoteCreate):
    id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class NoteDelete(NoteBase):
    id: int