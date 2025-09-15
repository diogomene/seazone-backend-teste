"""Configuração do banco de dados SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# URL de conexão do banco
DATABASE_URL = settings.database_url

# Criar engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,  # Log SQL queries em debug
    pool_size=10,
    max_overflow=20,
)

# Criar session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos SQLAlchemy
Base = declarative_base()


def get_database_session():
    """
    Dependency para obter sessão do banco de dados.
    Para ser usado com FastAPI Dependency Injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Criar todas as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Remover todas as tabelas do banco de dados."""
    Base.metadata.drop_all(bind=engine)