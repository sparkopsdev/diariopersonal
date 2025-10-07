from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Declaración y motor de SQLite (las tres barras son porque es un archivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./diario.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}   # Permite varias peticiones simultáneas.
)

# Crear sesión de trabajo con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base que usarán los modelos (User, Note)
Base = declarative_base()

# Dependencia común para FastAPI: obtener una sesión por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
