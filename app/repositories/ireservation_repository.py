"""Interface para repositório de reservas."""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from app.entities.reservation import Reservation
from app.dtos.reservation_dtos import ReservationFiltersDTO


class IReservationRepository(ABC):
    """Interface para repositório de reservas."""
    
    @abstractmethod
    async def create(self, reservation_data: dict) -> Reservation:
        """
        Criar uma nova reserva.
        
        Args:
            reservation_data: Dados da reserva
            
        Returns:
            Reservation: Reserva criada
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Buscar reserva por ID.
        
        Args:
            reservation_id: ID da reserva
            
        Returns:
            Optional[Reservation]: Reserva encontrada ou None
        """
        pass
    
    @abstractmethod
    async def get_all(self, filters: ReservationFiltersDTO, offset: int = 0, limit: int = 100) -> List[Reservation]:
        """
        Listar reservas com filtros.
        
        Args:
            filters: Filtros de busca
            offset: Offset para paginação
            limit: Limite de registros
            
        Returns:
            List[Reservation]: Lista de reservas
        """
        pass
    
    @abstractmethod
    async def get_with_details(self, reservation_id: int) -> Optional[dict]:
        """
        Buscar reserva com detalhes completos (propriedade e cliente).
        
        Args:
            reservation_id: ID da reserva
            
        Returns:
            Optional[dict]: Dict com reserva, propriedade e cliente ou None
        """
        pass
    
    @abstractmethod
    async def get_conflicting_reservations(
        self, 
        property_id: int, 
        start_date: date, 
        end_date: date,
        exclude_reservation_id: Optional[int] = None
    ) -> List[Reservation]:
        """
        Buscar reservas que conflitam com o período especificado.
        
        Args:
            property_id: ID da propriedade
            start_date: Data de início
            end_date: Data de fim
            exclude_reservation_id: ID da reserva para excluir da busca (para atualizações)
            
        Returns:
            List[Reservation]: Lista de reservas conflitantes
        """
        pass
    
    @abstractmethod
    async def cancel(self, reservation_id: int) -> bool:
        """
        Cancelar uma reserva (marcar como inativa).
        
        Args:
            reservation_id: ID da reserva
            
        Returns:
            bool: True se cancelada com sucesso, False se não encontrada
        """
        pass
    
    @abstractmethod
    async def exists(self, reservation_id: int) -> bool:
        """
        Verificar se reserva existe.
        
        Args:
            reservation_id: ID da reserva
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass