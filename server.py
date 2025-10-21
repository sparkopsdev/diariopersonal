from fastapi import FastAPI
from database import Base, engine
from api.user import router as user_router
from api.note import router as note_router

# Crear las tablas (si no existen)
Base.metadata.create_all(bind=engine)

# Inicializar la app principal
app = FastAPI(
    title="Notas API",
    description="API para gestionar usuarios y notas basadas en archivos locales.",
    version="1.0.0"
)

# Incluir routers
app.include_router(user_router)
app.include_router(note_router)

@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de Notas y Usuarios. Usa /docs para probar los endpoints."
    }