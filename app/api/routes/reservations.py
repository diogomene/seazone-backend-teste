"""Rotas para reservas."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database import get_database_session
from app.controller.reservation_controller import ReservationController
from app.dtos.reservation_dtos import (
    ReservationCreateDTO,
    ReservationResponseDTO,
    ReservationListDTO,
    ReservationCancelDTO
)

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def get_reservation_controller(session: Session = Depends(get_database_session)) -> ReservationController:
    """Dependency para obter controlador de reservas."""
    return ReservationController(session)


@router.post("/", response_model=ReservationResponseDTO, status_code=201)
async def create_reservation(
    reservation_data: ReservationCreateDTO,
    controller: ReservationController = Depends(get_reservation_controller)
):
    """
    Criar uma nova reserva.
    
    **Validações realizadas automaticamente:**
    - Propriedade deve existir
    - Data de fim deve ser posterior à data de início
    - Data de início não pode ser no passado
    - Propriedade deve estar disponível nas datas solicitadas
    - Quantidade de hóspedes não pode exceder a capacidade da propriedade
    - Preço é calculado automaticamente (dias × preço_por_noite)
    - Cliente é criado automaticamente se não existir
    
    **Campos obrigatórios:**
    - **property_id**: ID da propriedade
    - **client_name**: Nome do cliente
    - **client_email**: Email do cliente (formato válido)
    - **start_date**: Data de início (formato: YYYY-MM-DD)
    - **end_date**: Data de fim (formato: YYYY-MM-DD)
    - **guests_quantity**: Quantidade de hóspedes (> 0)
    """
    return await controller.create_reservation(reservation_data)


@router.get("/", response_model=List[ReservationListDTO])
async def list_reservations(
    controller: ReservationController = Depends(get_reservation_controller),
    client_email: Optional[str] = Query(None, description="Filtro por email do cliente"),
    property_id: Optional[int] = Query(None, ge=1, description="Filtro por ID da propriedade"),
    active_only: bool = Query(True, description="Mostrar apenas reservas ativas"),
    page: int = Query(1, ge=1, description="Página (começando em 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página (1-100)")
):
    """
    Listar reservas com filtros opcionais.
    
    **Filtros disponíveis:**
    - **client_email**: Buscar reservas de um cliente específico
    - **property_id**: Buscar reservas de uma propriedade específica
    - **active_only**: Mostrar apenas reservas ativas (padrão: true)
    
    **Paginação:**
    - **page**: Número da página (padrão: 1)
    - **page_size**: Quantidade de itens por página (padrão: 20, máximo: 100)
    
    **Nota:** Pelo menos um dos filtros (client_email ou property_id) é recomendado
    para evitar listagens muito grandes.
    """
    return await controller.list_reservations(
        client_email=client_email,
        property_id=property_id,
        active_only=active_only,
        page=page,
        page_size=page_size
    )


@router.delete("/{reservation_id}", response_model=ReservationCancelDTO)
async def cancel_reservation(
    reservation_id: int,
    controller: ReservationController = Depends(get_reservation_controller)
):
    """
    Cancelar uma reserva existente.
    
    **Operação:**
    - Marca a reserva como inativa (soft delete)
    - A reserva permanece no banco de dados para histórico
    - Reservas canceladas liberam a propriedade para novas reservas
    
    **Parâmetros:**
    - **reservation_id**: ID da reserva a ser cancelada
    
    **Retorna:**
    - Informações sobre o sucesso ou falha do cancelamento
    - Mensagem explicativa do resultado
    """
    return await controller.cancel_reservation(reservation_id)