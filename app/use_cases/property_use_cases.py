"""Use cases para propriedades."""

from typing import List, Optional
from datetime import date

from app.repositories.iproperty_repository import IPropertyRepository
from app.dtos.property_dtos import (
    PropertyCreateDTO, 
    PropertyResponseDTO, 
    PropertyListDTO, 
    PropertyFiltersDTO,
    PropertyAvailabilityDTO
)


class CriarPropriedadeUseCase:
    """Use case para criar uma propriedade."""
    
    def __init__(self, property_repository: IPropertyRepository):
        self.property_repository = property_repository
    
    async def execute(self, property_data: PropertyCreateDTO) -> PropertyResponseDTO:
        """
        Executar criação de propriedade.
        
        Args:
            property_data: Dados da propriedade
            
        Returns:
            PropertyResponseDTO: Propriedade criada
        """
        address_data = {
            "street": property_data.address_street,
            "number": property_data.address_number,
            "neighborhood": property_data.address_neighborhood,
            "city": property_data.address_city,
            "state": property_data.address_state,
            "country": property_data.country
        }
        
        property_obj_data = {
            "title": property_data.title,
            "rooms": property_data.rooms,
            "capacity": property_data.capacity,
            "price_per_night": property_data.price_per_night
        }
        
        property_obj = await self.property_repository.create(property_obj_data, address_data)
        
        property_with_address = await self.property_repository.get_with_address(property_obj.id)  # type: ignore
        
        if not property_with_address:
            raise ValueError("Erro ao recuperar propriedade criada")
        
        property_obj, address_obj = property_with_address
        
        from app.dtos.property_dtos import AddressResponseDTO
        address_dto = AddressResponseDTO.model_validate(address_obj)
        
        return PropertyResponseDTO(
            id=property_obj.id,  # type: ignore
            title=property_obj.title,  # type: ignore
            address=address_dto,
            rooms=property_obj.rooms,  # type: ignore
            capacity=property_obj.capacity,  # type: ignore
            price_per_night=property_obj.price_per_night,  # type: ignore
            created_at=property_obj.created_at,  # type: ignore
            updated_at=property_obj.updated_at  # type: ignore
        )


class ListarPropriedadesUseCase:
    """Use case para listar propriedades."""
    
    def __init__(self, property_repository: IPropertyRepository):
        self.property_repository = property_repository
    
    async def execute(
        self, 
        filters: PropertyFiltersDTO, 
        page: int = 1, 
        page_size: int = 20
    ) -> List[PropertyListDTO]:
        """
        Executar listagem de propriedades.
        
        Args:
            filters: Filtros de busca
            page: Página (1-indexed)
            page_size: Tamanho da página
            
        Returns:
            List[PropertyListDTO]: Lista de propriedades
        """
        offset = (page - 1) * page_size
        
        properties = await self.property_repository.get_all(filters, offset, page_size)
        
        result = []
        for property_obj in properties:
            if hasattr(property_obj, 'address') and property_obj.address:
                address_obj = property_obj.address
                property_dto = PropertyListDTO.from_property_with_address(property_obj, address_obj)
                result.append(property_dto)
        
        return result


class VerificarDisponibilidadeUseCase:
    """Use case para verificar disponibilidade de propriedade."""
    
    def __init__(self, property_repository: IPropertyRepository):
        self.property_repository = property_repository
    
    async def execute(
        self, 
        property_id: int, 
        start_date: date, 
        end_date: date, 
        guests_quantity: int
    ) -> PropertyAvailabilityDTO:
        """
        Executar verificação de disponibilidade.
        
        Args:
            property_id: ID da propriedade
            start_date: Data de início
            end_date: Data de fim
            guests_quantity: Quantidade de hóspedes
            
        Returns:
            PropertyAvailabilityDTO: Resultado da verificação
        """
        if not await self.property_repository.exists(property_id):
            return PropertyAvailabilityDTO(
                property_id=property_id,
                available=False,
                message="Propriedade não encontrada"
            )
        
        availability_result = await self.property_repository.check_availability(
            property_id, start_date, end_date, guests_quantity
        )
        
        return PropertyAvailabilityDTO(
            property_id=property_id,
            available=availability_result["available"],
            message=availability_result["message"],
            conflicting_reservations=availability_result.get("conflicting_reservations")
        )