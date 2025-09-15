"""DTOs para reservas."""

from typing import Optional
from decimal import Decimal
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator


class ReservationCreateDTO(BaseModel):
    """DTO para criar uma reserva."""
    
    property_id: int = Field(..., gt=0, description="ID da propriedade")
    client_name: str = Field(..., min_length=1, max_length=255, description="Nome do cliente")
    client_email: str = Field(..., min_length=5, max_length=255, description="Email do cliente")
    start_date: date = Field(..., description="Data de início da reserva")
    end_date: date = Field(..., description="Data de fim da reserva")
    guests_quantity: int = Field(..., gt=0, description="Quantidade de hóspedes")
    
    @field_validator('client_email')
    @classmethod
    def validate_email(cls, v):
        """Validar formato do email."""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Email inválido')
        return v.lower()
    
    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v, info):
        """Validar se a data de fim é posterior à data de início."""
        if info.data.get('start_date') and v <= info.data['start_date']:
            raise ValueError('A data de fim deve ser posterior à data de início')
        return v
    
    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v):
        """Validar se a data de início não é no passado."""
        from datetime import date
        if v < date.today():
            raise ValueError('A data de início não pode ser no passado')
        return v
    
    class Config:
        from_attributes = True


class ClientResponseDTO(BaseModel):
    """DTO para resposta de cliente."""
    
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


class PropertySummaryDTO(BaseModel):
    """DTO para resumo de propriedade nas reservas."""
    
    id: int
    title: str
    city: str
    state: str
    
    class Config:
        from_attributes = True


class ReservationResponseDTO(BaseModel):
    """DTO para resposta completa de reserva."""
    
    id: int
    property: PropertySummaryDTO
    client: ClientResponseDTO
    start_date: date
    end_date: date
    guests_quantity: int
    price: Decimal
    active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ReservationListDTO(BaseModel):
    """DTO para listagem de reservas (versão simplificada)."""
    
    id: int
    property_title: str
    client_name: str
    client_email: str
    start_date: date
    end_date: date
    guests_quantity: int
    price: Decimal
    active: bool
    
    @classmethod
    def from_reservation_with_details(cls, reservation_obj, property_obj, client_obj):
        """Criar DTO a partir de objetos Reservation, Property e Client."""
        return cls(
            id=reservation_obj.id,
            property_title=property_obj.title,
            client_name=client_obj.name,
            client_email=client_obj.email,
            start_date=reservation_obj.start_date,
            end_date=reservation_obj.end_date,
            guests_quantity=reservation_obj.guests_quantity,
            price=reservation_obj.price,
            active=reservation_obj.active
        )
    
    class Config:
        from_attributes = True


class ReservationFiltersDTO(BaseModel):
    """DTO para filtros de busca de reservas."""
    
    client_email: Optional[str] = None
    property_id: Optional[int] = None
    active_only: bool = True
    
    @field_validator('client_email')
    @classmethod
    def validate_client_email(cls, v):
        """Validar formato do email quando fornecido."""
        if v is not None:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Email inválido')
            return v.lower()
        return v
    
    @field_validator('property_id')
    @classmethod
    def validate_property_id(cls, v):
        """Validar ID da propriedade."""
        if v is not None and v <= 0:
            raise ValueError('ID da propriedade deve ser maior que zero')
        return v
    
    class Config:
        from_attributes = True


class ReservationCancelDTO(BaseModel):
    """DTO para confirmação de cancelamento de reserva."""
    
    id: int
    cancelled: bool
    message: str
    
    class Config:
        from_attributes = True