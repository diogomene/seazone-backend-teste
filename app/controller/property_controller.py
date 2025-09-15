"""Controlador para propriedades."""

from typing import List, Optional
from datetime import date
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.use_cases.property_use_cases import (
    CriarPropriedadeUseCase,
    ListarPropriedadesUseCase,
    VerificarDisponibilidadeUseCase
)
from app.infrastructure.repositories.sqlalchemy_property_repository import SQLAlchemyPropertyRepository
from app.dtos.property_dtos import (
    PropertyCreateDTO,
    PropertyResponseDTO,
    PropertyListDTO,
    PropertyFiltersDTO,
    PropertyAvailabilityDTO
)


class PropertyController:
    """Controlador para operações de propriedades."""
    
    def __init__(self, session: Session):
        self.session = session
        self.property_repository = SQLAlchemyPropertyRepository(session)
        
        self.criar_propriedade_use_case = CriarPropriedadeUseCase(self.property_repository)
        self.listar_propriedades_use_case = ListarPropriedadesUseCase(self.property_repository)
        self.verificar_disponibilidade_use_case = VerificarDisponibilidadeUseCase(self.property_repository)
    
    async def create_property(self, property_data: PropertyCreateDTO) -> PropertyResponseDTO:
        """
        Criar uma nova propriedade.
        
        Args:
            property_data: Dados da propriedade
            
        Returns:
            PropertyResponseDTO: Propriedade criada
            
        Raises:
            HTTPException: Em caso de erro na criação
        """
        try:
            return await self.criar_propriedade_use_case.execute(property_data)
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
    
    async def list_properties(
        self,
        city: Optional[str] = None,
        state: Optional[str] = None,
        neighborhood: Optional[str] = None,
        max_capacity: Optional[int] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[PropertyListDTO]:
        """
        Listar propriedades com filtros.
        
        Args:
            city: Filtro por cidade
            state: Filtro por estado
            neighborhood: Filtro por bairro
            max_capacity: Capacidade máxima
            max_price: Preço máximo
            page: Página (1-indexed)
            page_size: Tamanho da página
            
        Returns:
            List[PropertyListDTO]: Lista de propriedades
            
        Raises:
            HTTPException: Em caso de erro na listagem
        """
        try:
            max_price_decimal = None
            if max_price is not None:
                max_price_decimal = Decimal(str(max_price))
            
            filters = PropertyFiltersDTO(
                city=city,
                state=state,
                neighborhood=neighborhood,
                max_capacity=max_capacity,
                max_price=max_price_decimal
            )
            
            return await self.listar_propriedades_use_case.execute(filters, page, page_size)
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
    
    async def check_availability(
        self,
        property_id: int,
        start_date: date,
        end_date: date,
        guests_quantity: int
    ) -> PropertyAvailabilityDTO:
        """
        Verificar disponibilidade de uma propriedade.
        
        Args:
            property_id: ID da propriedade
            start_date: Data de início
            end_date: Data de fim
            guests_quantity: Quantidade de hóspedes
            
        Returns:
            PropertyAvailabilityDTO: Resultado da verificação
            
        Raises:
            HTTPException: Em caso de erro na verificação
        """
        try:
            # Validar datas
            if start_date >= end_date:
                raise ValueError("A data de fim deve ser posterior à data de início")
            
            if guests_quantity <= 0:
                raise ValueError("A quantidade de hóspedes deve ser maior que zero")
            
            return await self.verificar_disponibilidade_use_case.execute(
                property_id, start_date, end_date, guests_quantity
            )
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