"""Entidade Address - Modelo SQLAlchemy."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class Address(Base):
    """Modelo SQLAlchemy para endereços."""
    
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(255), nullable=False)
    number = Column(String(20), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False, default="Brasil")
    
    properties = relationship("Property", back_populates="address")
