"""
Clase: 
    Note
Tipo:
    Modelo SQLite
Descripción:
    Esta clase define el modelo de las notas y su relación con la clase "User" para la base de datos.
"""

# Paquetes externos
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Paquetes internos
from database import Base

class Note(Base):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)       # Primary key del usuario (campo id en "User")
    user = relationship("User", back_populates="notes")                     # Relación con el campo "notes" de la instancia del usuario
