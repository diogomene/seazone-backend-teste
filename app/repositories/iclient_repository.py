"""Interface para repositório de clientes."""

from abc import ABC, abstractmethod
from typing import Optional

from app.entities.client import Client


class IClientRepository(ABC):
    """Interface para repositório de clientes."""
    
    @abstractmethod
    async def create(self, client_data: dict) -> Client:
        """
        Criar um novo cliente.
        
        Args:
            client_data: Dados do cliente
            
        Returns:
            Client: Cliente criado
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Buscar cliente por ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Optional[Client]: Cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Client]:
        """
        Buscar cliente por email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Optional[Client]: Cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_or_create_by_email(self, name: str, email: str) -> Client:
        """
        Buscar cliente por email ou criar se não existir.
        
        Args:
            name: Nome do cliente
            email: Email do cliente
            
        Returns:
            Client: Cliente encontrado ou criado
        """
        pass
    
    @abstractmethod
    async def exists(self, client_id: int) -> bool:
        """
        Verificar se cliente existe.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """
        Verificar se cliente existe por email.
        
        Args:
            email: Email do cliente
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass