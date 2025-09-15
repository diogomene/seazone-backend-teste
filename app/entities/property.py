"""Entidade Property - Modelo SQLAlchemy."""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class Property(Base):
    """Modelo SQLAlchemy para propriedades."""
    
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    rooms = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    address = relationship("Address", back_populates="properties")
