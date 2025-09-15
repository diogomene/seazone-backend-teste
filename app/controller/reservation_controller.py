"""Controlador para reservas."""

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.use_cases.reservation_use_cases import (
    CriarReservaUseCase,
    ListarReservasUseCase,
    CancelarReservaUseCase
)
from app.infrastructure.repositories.sqlalchemy_reservation_repository import SQLAlchemyReservationRepository
from app.infrastructure.repositories.sqlalchemy_property_repository import SQLAlchemyPropertyRepository
from app.infrastructure.repositories.sqlalchemy_client_repository import SQLAlchemyClientRepository
from app.dtos.reservation_dtos import (
    ReservationCreateDTO,
    ReservationResponseDTO,
    ReservationListDTO,
    ReservationFiltersDTO,
    ReservationCancelDTO
)


class ReservationController:
    """Controlador para operações de reservas."""
    
    def __init__(self, session: Session):
        self.session = session
        
        self.reservation_repository = SQLAlchemyReservationRepository(session)
        self.property_repository = SQLAlchemyPropertyRepository(session)
        self.client_repository = SQLAlchemyClientRepository(session)
        
        self.criar_reserva_use_case = CriarReservaUseCase(
            self.reservation_repository,
            self.property_repository,
            self.client_repository
        )
        self.listar_reservas_use_case = ListarReservasUseCase(self.reservation_repository)
        self.cancelar_reserva_use_case = CancelarReservaUseCase(self.reservation_repository)
    
    async def create_reservation(self, reservation_data: ReservationCreateDTO) -> ReservationResponseDTO:
        """
        Criar uma nova reserva.
        
        Args:
            reservation_data: Dados da reserva
            
        Returns:
            ReservationResponseDTO: Reserva criada
            
        Raises:
            HTTPException: Em caso de erro na criação
        """
        try:
            return await self.criar_reserva_use_case.execute(reservation_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def list_reservations(
        self,
        client_email: Optional[str] = None,
        property_id: Optional[int] = None,
        active_only: bool = True,
        page: int = 1,
        page_size: int = 20
    ) -> List[ReservationListDTO]:
        """
        Listar reservas com filtros.
        
        Args:
            client_email: Filtro por email do cliente
            property_id: Filtro por ID da propriedade
            active_only: Mostrar apenas reservas ativas
            page: Página (1-indexed)
            page_size: Tamanho da página
            
        Returns:
            List[ReservationListDTO]: Lista de reservas
            
        Raises:
            HTTPException: Em caso de erro na listagem
        """
        try:
            # Montar filtros
            filters = ReservationFiltersDTO(
                client_email=client_email,
                property_id=property_id,
                active_only=active_only
            )
            
            return await self.listar_reservas_use_case.execute(filters, page, page_size)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def cancel_reservation(self, reservation_id: int) -> ReservationCancelDTO:
        """
        Cancelar uma reserva.
        
        Args:
            reservation_id: ID da reserva
            
        Returns:
            ReservationCancelDTO: Resultado do cancelamento
            
        Raises:
            HTTPException: Em caso de erro no cancelamento
        """
        try:
            result = await self.cancelar_reserva_use_case.execute(reservation_id)
            
            # Se não foi cancelada por não encontrar, retornar 404
            if not result.cancelled and "não encontrada" in result.message:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=result.message
                )
            
            return result
        except HTTPException:
            raise  # Re-lançar HTTPException
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )