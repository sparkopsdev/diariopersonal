# Paquetes externos
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Paquetes internos
from database import get_db
from model.user import User
from validate.user import *

router = APIRouter(prefix="/users", tags=["Users"])

"""
Creación de usuario.
"""
@router.post("", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def createUser(user: UserCreate, db: Session = Depends(get_db)):

    # Si el correo existe, da error porque ya está el usuario creado
    existingUser = db.query(User).filter(User.email == user.email).first()
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    # Creación del nuevo usuario validando con "UserCreate"
    newUser = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    # Persistencia en SQLite
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

"""
Listado de usuarios.
"""
@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def listUsers(db: Session = Depends(get_db)):

    userList = db.query(User).all()
    return userList
