"""Entidade Reservation - Modelo SQLAlchemy."""

from sqlalchemy import Column, Integer, Date, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class Reservation(Base):
    """Modelo SQLAlchemy para reservas."""
    
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    guests_quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    property = relationship("Property")
    client = relationship("Client")
