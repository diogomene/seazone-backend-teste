"""DTOs para propriedades."""

from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class PropertyCreateDTO(BaseModel):
    """DTO para criar uma propriedade."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Título da propriedade")
    address_street: str = Field(..., min_length=1, max_length=255, description="Logradouro do endereço")
    address_number: str = Field(..., min_length=1, max_length=20, description="Número do endereço")
    address_neighborhood: str = Field(..., min_length=1, max_length=100, description="Bairro")
    address_city: str = Field(..., min_length=1, max_length=100, description="Cidade")
    address_state: str = Field(..., min_length=1, max_length=50, description="Estado")
    country: str = Field(default="Brasil", min_length=1, max_length=50, description="País")
    rooms: int = Field(..., gt=0, description="Quantidade de quartos")
    capacity: int = Field(..., gt=0, description="Capacidade máxima de pessoas")
    price_per_night: Decimal = Field(..., gt=0, description="Preço por noite")
    
    @field_validator('price_per_night')
    @classmethod
    def validate_price(cls, v):
        """Validar se o preço tem no máximo 2 casas decimais."""
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero')
        # Verificar se tem no máximo 2 casas decimais
        if v.as_tuple().exponent < -2:
            raise ValueError('O preço deve ter no máximo 2 casas decimais')
        return v
    
    class Config:
        from_attributes = True


class AddressResponseDTO(BaseModel):
    """DTO para resposta de endereço."""
    
    id: int
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    country: str
    
    class Config:
        from_attributes = True


class PropertyResponseDTO(BaseModel):
    """DTO para resposta completa de propriedade."""
    
    id: int
    title: str
    address: AddressResponseDTO
    rooms: int
    capacity: int
    price_per_night: Decimal
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PropertyListDTO(BaseModel):
    """DTO para listagem de propriedades (versão simplificada)."""
    
    id: int
    title: str
    city: str
    state: str
    neighborhood: str
    rooms: int
    capacity: int
    price_per_night: Decimal
    
    @classmethod
    def from_property_with_address(cls, property_obj, address_obj):
        """Criar DTO a partir de objetos Property e Address."""
        return cls(
            id=property_obj.id,
            title=property_obj.title,
            city=address_obj.city,
            state=address_obj.state,
            neighborhood=address_obj.neighborhood,
            rooms=property_obj.rooms,
            capacity=property_obj.capacity,
            price_per_night=property_obj.price_per_night
        )
    
    class Config:
        from_attributes = True


class PropertyAvailabilityDTO(BaseModel):
    """DTO para resposta de disponibilidade de propriedade."""
    
    property_id: int
    available: bool
    message: str
    conflicting_reservations: Optional[list] = None
    
    class Config:
        from_attributes = True


class PropertyFiltersDTO(BaseModel):
    """DTO para filtros de busca de propriedades."""
    
    city: Optional[str] = None
    state: Optional[str] = None
    neighborhood: Optional[str] = None
    max_capacity: Optional[int] = None
    max_price: Optional[Decimal] = None
    
    @field_validator('max_capacity')
    @classmethod
    def validate_max_capacity(cls, v):
        """Validar capacidade máxima."""
        if v is not None and v <= 0:
            raise ValueError('A capacidade máxima deve ser maior que zero')
        return v
    
    @field_validator('max_price')
    @classmethod
    def validate_max_price(cls, v):
        """Validar preço máximo."""
        if v is not None and v <= 0:
            raise ValueError('O preço máximo deve ser maior que zero')
        return v
    
    class Config:
        from_attributes = True