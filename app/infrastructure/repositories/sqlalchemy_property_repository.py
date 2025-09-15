"""Implementação SQLAlchemy do repositório de propriedades."""

from typing import List, Optional, Union
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.repositories.iproperty_repository import IPropertyRepository
from app.entities.property import Property
from app.entities.address import Address
from app.entities.reservation import Reservation
from app.dtos.property_dtos import PropertyFiltersDTO


class SQLAlchemyPropertyRepository(IPropertyRepository):
    """Implementação SQLAlchemy do repositório de propriedades."""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, property_data: dict, address_data: dict) -> Property:
        """Criar uma nova propriedade com seu endereço."""
        address = Address(**address_data)
        self.session.add(address)
        self.session.flush()  
        
        property_data['address_id'] = address.id
        property_obj = Property(**property_data)
        self.session.add(property_obj)
        self.session.commit()
        
        self.session.refresh(property_obj)
        return property_obj
    
    async def get_by_id(self, property_id: int) -> Optional[Property]:
        """Buscar propriedade por ID."""
        return self.session.query(Property).filter(Property.id == property_id).first()
    
    async def get_all(self, filters: PropertyFiltersDTO, offset: int = 0, limit: int = 100) -> List[Property]:
        """Listar propriedades com filtros."""
        query = self.session.query(Property).join(Address)
        
        if filters.city:
            query = query.filter(func.lower(Address.city).like(f"%{filters.city.lower()}%"))
        
        if filters.state:
            query = query.filter(func.lower(Address.state).like(f"%{filters.state.lower()}%"))
        
        if filters.neighborhood:
            query = query.filter(func.lower(Address.neighborhood).like(f"%{filters.neighborhood.lower()}%"))
        
        if filters.max_capacity:
            query = query.filter(Property.capacity <= filters.max_capacity)
        
        if filters.max_price:
            query = query.filter(Property.price_per_night <= filters.max_price)
        
        query = query.offset(offset).limit(limit)
        
        query = query.options(joinedload(Property.address))
        
        return query.all()
    
    async def get_with_address(self, property_id: int) -> Optional[tuple[Property, Address]]:
        """Buscar propriedade com endereço por ID."""
        result = (
            self.session.query(Property, Address)
            .join(Address)
            .filter(Property.id == property_id)
            .first()
        )
        if result:
            return (result[0], result[1])
        return None
    
    async def check_availability(
        self, 
        property_id: int, 
        start_date: date, 
        end_date: date,
        guests_quantity: int
    ) -> dict:
        """Verificar disponibilidade de propriedade para datas específicas."""
        property_obj = self.session.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            return {
                "available": False,
                "message": "Propriedade não encontrada",
                "conflicting_reservations": []
            }
        
        conflicting_reservations = (
            self.session.query(Reservation)
            .filter(
                and_(
                    Reservation.property_id == property_id,
                    Reservation.active == True,
                    or_(
                        and_(
                            Reservation.start_date <= start_date,
                            Reservation.end_date >= start_date
                        ),
                        and_(
                            Reservation.start_date <= end_date,
                            Reservation.end_date >= end_date
                        ),
                        and_(
                            Reservation.start_date >= start_date,
                            Reservation.end_date <= end_date
                        ),
                        and_(
                            Reservation.start_date <= start_date,
                            Reservation.end_date >= end_date
                        )
                    )
                )
            )
            .all()
        )
        
        if conflicting_reservations:
            return {
                "available": False,
                "message": "Propriedade não disponível para as datas solicitadas",
                "conflicting_reservations": [
                    {
                        "id": res.id,
                        "start_date": res.start_date.isoformat(),
                        "end_date": res.end_date.isoformat()
                    }
                    for res in conflicting_reservations
                ]
            }
        
        capacity_result = self.session.query(Property.capacity).filter(Property.id == property_id).scalar()
        if capacity_result and guests_quantity > capacity_result:
            return {
                "available": False,
                "message": f"Capacidade excedida. Máximo: {capacity_result} hóspedes",
                "conflicting_reservations": []
            }
        
        return {
            "available": True,
            "message": "Propriedade disponível para as datas solicitadas",
            "conflicting_reservations": []
        }
    
    async def exists(self, property_id: int) -> bool:
        """Verificar se propriedade existe."""
        return self.session.query(Property).filter(Property.id == property_id).first() is not None