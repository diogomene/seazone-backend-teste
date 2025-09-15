"""Implementação SQLAlchemy do repositório de reservas."""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_

from app.repositories.ireservation_repository import IReservationRepository
from app.entities.reservation import Reservation
from app.entities.property import Property
from app.entities.client import Client
from app.entities.address import Address
from app.dtos.reservation_dtos import ReservationFiltersDTO


class SQLAlchemyReservationRepository(IReservationRepository):
    """Implementação SQLAlchemy do repositório de reservas."""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, reservation_data: dict) -> Reservation:
        """Criar uma nova reserva."""
        reservation = Reservation(**reservation_data)
        self.session.add(reservation)
        self.session.commit()
        self.session.refresh(reservation)
        return reservation
    
    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """Buscar reserva por ID."""
        return self.session.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    async def get_all(self, filters: ReservationFiltersDTO, offset: int = 0, limit: int = 100) -> List[Reservation]:
        """Listar reservas com filtros."""
        query = self.session.query(Reservation)
        
        if filters.client_email:
            query = query.join(Client).filter(Client.email == filters.client_email)
        
        if filters.property_id:
            query = query.filter(Reservation.property_id == filters.property_id)
        
        if filters.active_only:
            query = query.filter(Reservation.active == True)

        query = query.offset(offset).limit(limit)
        
        query = query.options(
            joinedload(Reservation.property),
            joinedload(Reservation.client)
        )
        
        return query.all()
    
    async def get_with_details(self, reservation_id: int) -> Optional[dict]:
        """Buscar reserva com detalhes completos (propriedade e cliente)."""
        result = (
            self.session.query(Reservation, Property, Client, Address)
            .join(Property, Reservation.property_id == Property.id)
            .join(Client, Reservation.client_id == Client.id)
            .join(Address, Property.address_id == Address.id)
            .filter(Reservation.id == reservation_id)
            .first()
        )
        
        if result:
            reservation, property_obj, client, address = result
            return {
                "reservation": reservation,
                "property": property_obj,
                "client": client,
                "address": address
            }
        return None
    
    async def get_conflicting_reservations(
        self, 
        property_id: int, 
        start_date: date, 
        end_date: date,
        exclude_reservation_id: Optional[int] = None
    ) -> List[Reservation]:
        """Buscar reservas que conflitam com o período especificado."""
        query = self.session.query(Reservation).filter(
            and_(
                Reservation.property_id == property_id,
                Reservation.active == True,
                or_(
                    and_(
                        Reservation.start_date <= start_date,
                        Reservation.end_date > start_date
                    ),
                    and_(
                        Reservation.start_date < end_date,
                        Reservation.end_date >= end_date
                    ),
                    and_(
                        Reservation.start_date >= start_date,
                        Reservation.end_date <= end_date
                    )
                )
            )
        )
        
        if exclude_reservation_id:
            query = query.filter(Reservation.id != exclude_reservation_id)
        
        return query.all()
    
    async def cancel(self, reservation_id: int) -> bool:
        """Cancelar uma reserva (marcar como inativa)."""
        updated = (
            self.session.query(Reservation)
            .filter(Reservation.id == reservation_id)
            .update({"active": False})
        )
        
        if updated > 0:
            self.session.commit()
            return True
        
        return False
    
    async def exists(self, reservation_id: int) -> bool:
        """Verificar se reserva existe."""
        return self.session.query(Reservation).filter(Reservation.id == reservation_id).first() is not None