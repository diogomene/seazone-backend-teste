"""Interface para repositório de propriedades."""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from app.entities.property import Property
from app.entities.address import Address
from app.dtos.property_dtos import PropertyFiltersDTO


class IPropertyRepository(ABC):
    """Interface para repositório de propriedades."""
    
    @abstractmethod
    async def create(self, property_data: dict, address_data: dict) -> Property:
        """
        Criar uma nova propriedade com seu endereço.
        
        Args:
            property_data: Dados da propriedade
            address_data: Dados do endereço
            
        Returns:
            Property: Propriedade criada
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, property_id: int) -> Optional[Property]:
        """
        Buscar propriedade por ID.
        
        Args:
            property_id: ID da propriedade
            
        Returns:
            Optional[Property]: Propriedade encontrada ou None
        """
        pass
    
    @abstractmethod
    async def get_all(self, filters: PropertyFiltersDTO, offset: int = 0, limit: int = 100) -> List[Property]:
        """
        Listar propriedades com filtros.
        
        Args:
            filters: Filtros de busca
            offset: Offset para paginação
            limit: Limite de registros
            
        Returns:
            List[Property]: Lista de propriedades
        """
        pass
    
    @abstractmethod
    async def get_with_address(self, property_id: int) -> Optional[tuple[Property, Address]]:
        """
        Buscar propriedade com endereço por ID.
        
        Args:
            property_id: ID da propriedade
            
        Returns:
            Optional[tuple[Property, Address]]: Tupla (propriedade, endereço) ou None
        """
        pass
    
    @abstractmethod
    async def check_availability(
        self, 
        property_id: int, 
        start_date: date, 
        end_date: date,
        guests_quantity: int
    ) -> dict:
        """
        Verificar disponibilidade de propriedade para datas específicas.
        
        Args:
            property_id: ID da propriedade
            start_date: Data de início
            end_date: Data de fim
            guests_quantity: Quantidade de hóspedes
            
        Returns:
            dict: Resultado da verificação com informações de disponibilidade
        """
        pass
    
    @abstractmethod
    async def exists(self, property_id: int) -> bool:
        """
        Verificar se propriedade existe.
        
        Args:
            property_id: ID da propriedade
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass