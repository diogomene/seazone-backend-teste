"""Use cases para reservas."""

from typing import List
from decimal import Decimal

from app.repositories.ireservation_repository import IReservationRepository
from app.repositories.iproperty_repository import IPropertyRepository
from app.repositories.iclient_repository import IClientRepository
from app.dtos.reservation_dtos import (
    ReservationCreateDTO,
    ReservationResponseDTO,
    ReservationListDTO,
    ReservationFiltersDTO,
    ReservationCancelDTO
)


class CriarReservaUseCase:
    """Use case para criar uma reserva com validações."""
    
    def __init__(
        self, 
        reservation_repository: IReservationRepository,
        property_repository: IPropertyRepository,
        client_repository: IClientRepository
    ):
        self.reservation_repository = reservation_repository
        self.property_repository = property_repository
        self.client_repository = client_repository
    
    async def execute(self, reservation_data: ReservationCreateDTO) -> ReservationResponseDTO:
        """
        Executar criação de reserva com todas as validações.
        
        Args:
            reservation_data: Dados da reserva
            
        Returns:
            ReservationResponseDTO: Reserva criada
            
        Raises:
            ValueError: Em caso de validação falhou
        """
        if not await self.property_repository.exists(reservation_data.property_id):
            raise ValueError("Propriedade não encontrada")
        
        availability = await self.property_repository.check_availability(
            reservation_data.property_id,
            reservation_data.start_date,
            reservation_data.end_date,
            reservation_data.guests_quantity
        )
        
        if not availability["available"]:
            raise ValueError(availability["message"])
        
        client = await self.client_repository.get_or_create_by_email(
            reservation_data.client_name,
            reservation_data.client_email
        )
        
        property_obj = await self.property_repository.get_by_id(reservation_data.property_id)
        if not property_obj:
            raise ValueError("Erro ao buscar dados da propriedade")
        
        days = (reservation_data.end_date - reservation_data.start_date).days
        total_price = property_obj.price_per_night * days  # type: ignore
        
        reservation_obj_data = {
            "property_id": reservation_data.property_id,
            "client_id": client.id,  # type: ignore
            "start_date": reservation_data.start_date,
            "end_date": reservation_data.end_date,
            "guests_quantity": reservation_data.guests_quantity,
            "price": total_price,
            "active": True
        }
        
        reservation = await self.reservation_repository.create(reservation_obj_data)
        
        reservation_details = await self.reservation_repository.get_with_details(reservation.id)  # type: ignore
        
        if not reservation_details:
            raise ValueError("Erro ao recuperar reserva criada")
        
        reservation_obj = reservation_details["reservation"]
        property_obj = reservation_details["property"]
        client_obj = reservation_details["client"]
        address_obj = reservation_details["address"]
        
        from app.dtos.reservation_dtos import PropertySummaryDTO, ClientResponseDTO
        
        property_summary = PropertySummaryDTO(
            id=property_obj.id,  # type: ignore
            title=property_obj.title,  # type: ignore
            city=address_obj.city,  # type: ignore
            state=address_obj.state  # type: ignore
        )
        
        client_response = ClientResponseDTO(
            id=client_obj.id,  # type: ignore
            name=client_obj.name,  # type: ignore
            email=client_obj.email  # type: ignore
        )
        
        return ReservationResponseDTO(
            id=reservation_obj.id,  # type: ignore
            property=property_summary,
            client=client_response,
            start_date=reservation_obj.start_date,  # type: ignore
            end_date=reservation_obj.end_date,  # type: ignore
            guests_quantity=reservation_obj.guests_quantity,  # type: ignore
            price=reservation_obj.price,  # type: ignore
            active=reservation_obj.active,  # type: ignore
            created_at=reservation_obj.created_at,  # type: ignore
            updated_at=reservation_obj.updated_at  # type: ignore
        )


class ListarReservasUseCase:
    """Use case para listar reservas."""
    
    def __init__(self, reservation_repository: IReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(
        self, 
        filters: ReservationFiltersDTO,
        page: int = 1,
        page_size: int = 20
    ) -> List[ReservationListDTO]:
        """
        Executar listagem de reservas.
        
        Args:
            filters: Filtros de busca
            page: Página (1-indexed)
            page_size: Tamanho da página
            
        Returns:
            List[ReservationListDTO]: Lista de reservas
        """
        offset = (page - 1) * page_size
        
        reservations = await self.reservation_repository.get_all(filters, offset, page_size)
        
        result = []
        for reservation in reservations:
            if hasattr(reservation, 'property') and hasattr(reservation, 'client'):
                property_obj = reservation.property  # type: ignore
                client_obj = reservation.client  # type: ignore
                
                reservation_dto = ReservationListDTO.from_reservation_with_details(
                    reservation, property_obj, client_obj
                )
                result.append(reservation_dto)
        
        return result


class CancelarReservaUseCase:
    """Use case para cancelar uma reserva."""
    
    def __init__(self, reservation_repository: IReservationRepository):
        self.reservation_repository = reservation_repository
    
    async def execute(self, reservation_id: int) -> ReservationCancelDTO:
        """
        Executar cancelamento de reserva.
        
        Args:
            reservation_id: ID da reserva
            
        Returns:
            ReservationCancelDTO: Resultado do cancelamento
        """
        if not await self.reservation_repository.exists(reservation_id):
            return ReservationCancelDTO(
                id=reservation_id,
                cancelled=False,
                message="Reserva não encontrada"
            )
        
        success = await self.reservation_repository.cancel(reservation_id)
        
        if success:
            return ReservationCancelDTO(
                id=reservation_id,
                cancelled=True,
                message="Reserva cancelada com sucesso"
            )
        else:
            return ReservationCancelDTO(
                id=reservation_id,
                cancelled=False,
                message="Erro ao cancelar reserva"
            )