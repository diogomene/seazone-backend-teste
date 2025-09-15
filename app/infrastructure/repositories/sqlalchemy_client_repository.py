"""Implementação SQLAlchemy do repositório de clientes."""

from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.iclient_repository import IClientRepository
from app.entities.client import Client


class SQLAlchemyClientRepository(IClientRepository):
    """Implementação SQLAlchemy do repositório de clientes."""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, client_data: dict) -> Client:
        """Criar um novo cliente."""
        client = Client(**client_data)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client
    
    async def get_by_id(self, client_id: int) -> Optional[Client]:
        """Buscar cliente por ID."""
        return self.session.query(Client).filter(Client.id == client_id).first()
    
    async def get_by_email(self, email: str) -> Optional[Client]:
        """Buscar cliente por email."""
        return self.session.query(Client).filter(Client.email == email.lower()).first()
    
    async def get_or_create_by_email(self, name: str, email: str) -> Client:
        """Buscar cliente por email ou criar se não existir."""
        existing_client = await self.get_by_email(email)
        
        if existing_client:
            return existing_client
        
        client_data = {
            "name": name,
            "email": email.lower()
        }
        return await self.create(client_data)
    
    async def exists(self, client_id: int) -> bool:
        """Verificar se cliente existe."""
        return self.session.query(Client).filter(Client.id == client_id).first() is not None
    
    async def exists_by_email(self, email: str) -> bool:
        """Verificar se cliente existe por email."""
        return self.session.query(Client).filter(Client.email == email.lower()).first() is not None