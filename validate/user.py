"""
Clase: 
    User
Tipo:
    Schema pydantic
Descripción:
    Esta clase define las validaciones pydantic de las entradas y salidas de la clase User.
"""
import re
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


# Validador del modelo base
class UserBase(BaseModel):
    name: str = Field(..., min_length=5, description="Nombre de usuario (mínimo 5 caracteres)")
    email: str = Field(..., min_length=5, description="Dirección de correo electrónico (mínimo 5 caracteres)")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")

# Validador para el endpoint de creación de usuarios
class UserCreate(UserBase):
    
    @field_validator("email")
    def correctEmailFormat(cls, value):
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        correctEmail = re.match(regex, value)
        if correctEmail:
            return value
        else:
            raise ValueError("Incorrect email format.")
    
    @field_validator("password")
    def minPasswordSecurity(cls, value):
        regex = r".*\d.*"
        passwordOk = re.match(regex, value)
        if passwordOk:
            return value
        else:
            raise ValueError("Add at least one number to your password")


# Validador para el endpoint de muestra de usuarios
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
