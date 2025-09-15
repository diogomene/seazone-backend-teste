"""Rotas para propriedades."""

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import get_database_session

from app.controller.property_controller import PropertyController
from app.dtos.property_dtos import (
    PropertyCreateDTO,
    PropertyResponseDTO,
    PropertyListDTO,
    PropertyAvailabilityDTO
)

router = APIRouter(prefix="/properties", tags=["Properties"])


def get_property_controller(session: Session = Depends(get_database_session)) -> PropertyController:
    """Dependency para obter controlador de propriedades."""
    return PropertyController(session)


@router.post("/", response_model=PropertyResponseDTO, status_code=201)
async def create_property(
    property_data: PropertyCreateDTO,
    controller: PropertyController = Depends(get_property_controller)
):
    """
    Criar uma nova propriedade.
    
    - **title**: Título da propriedade
    - **address_street**: Logradouro do endereço
    - **address_number**: Número do endereço
    - **address_neighborhood**: Bairro
    - **address_city**: Cidade
    - **address_state**: Estado
    - **country**: País (padrão: Brasil)
    - **rooms**: Quantidade de quartos
    - **capacity**: Capacidade máxima de pessoas
    - **price_per_night**: Preço por noite
    """
    return await controller.create_property(property_data)


@router.get("/", response_model=List[PropertyListDTO])
async def list_properties(
    controller: PropertyController = Depends(get_property_controller),
    city: Optional[str] = Query(None, description="Filtro por cidade"),
    state: Optional[str] = Query(None, description="Filtro por estado"),
    neighborhood: Optional[str] = Query(None, description="Filtro por bairro"),
    max_capacity: Optional[int] = Query(None, ge=1, description="Capacidade máxima"),
    max_price: Optional[float] = Query(None, gt=0, description="Preço máximo por noite"),
    page: int = Query(1, ge=1, description="Página (começando em 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página (1-100)")
):
    """
    Listar propriedades com filtros opcionais.
    
    **Filtros disponíveis:**
    - **city**: Busca por cidade (busca parcial, case-insensitive)
    - **state**: Busca por estado (busca parcial, case-insensitive)
    - **neighborhood**: Busca por bairro (busca parcial, case-insensitive)
    - **max_capacity**: Propriedades com capacidade até o valor especificado
    - **max_price**: Propriedades com preço por noite até o valor especificado
    
    **Paginação:**
    - **page**: Número da página (padrão: 1)
    - **page_size**: Quantidade de itens por página (padrão: 20, máximo: 100)
    """
    return await controller.list_properties(
        city=city,
        state=state,
        neighborhood=neighborhood,
        max_capacity=max_capacity,
        max_price=max_price,
        page=page,
        page_size=page_size
    )


@router.get("/{property_id}/availability", response_model=PropertyAvailabilityDTO)
async def check_property_availability(
    property_id: int,
    start_date: date = Query(..., description="Data de início da estadia"),
    end_date: date = Query(..., description="Data de fim da estadia"),
    guests_quantity: int = Query(..., ge=1, description="Quantidade de hóspedes"),
    controller: PropertyController = Depends(get_property_controller)
):
    """
    Verificar disponibilidade de uma propriedade para datas específicas.
    
    **Verificações realizadas:**
    - Existência da propriedade
    - Capacidade da propriedade vs. quantidade de hóspedes
    - Conflitos com reservas existentes
    
    **Parâmetros:**
    - **property_id**: ID da propriedade
    - **start_date**: Data de início da estadia (formato: YYYY-MM-DD)
    - **end_date**: Data de fim da estadia (formato: YYYY-MM-DD)
    - **guests_quantity**: Quantidade de hóspedes (deve ser > 0)
    """
    return await controller.check_availability(
        property_id=property_id,
        start_date=start_date,
        end_date=end_date,
        guests_quantity=guests_quantity
    )