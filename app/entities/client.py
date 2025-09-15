"""Entidade Client - Modelo SQLAlchemy."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class Client(Base):
    """Modelo SQLAlchemy para clientes."""
    
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
