"""
Clase: 
    User
Tipo:
    Modelo SQLite
Descripción:
    Esta clase define el modelo del usuario y su relación con la clase "Note" en la base de datos.
"""

# Paquetes externos
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Paquetes internos
from database import Base

class User(Base):

    __tablename__ = "users"

    # Campos de User:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")       # Relación con las instancias de la clase "Note". 
    #                               ^^^^^^^^            ^^^^^^
    #                           Campos de "Notes"     Qué le pasa a las notas del usuario si se borra