"""Initial migration

Revision ID: 52088570c5bd
Revises: 
Create Date: 2025-09-15 15:57:09.869110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52088570c5bd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Criar tabela addresses
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('street', sa.String(length=255), nullable=False),
        sa.Column('number', sa.String(length=20), nullable=False),
        sa.Column('neighborhood', sa.String(length=100), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=50), nullable=False),
        sa.Column('country', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_addresses_id'), 'addresses', ['id'], unique=False)
    
    # Criar tabela clients
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_clients_email'), 'clients', ['email'], unique=True)
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
    
    # Criar tabela properties
    op.create_table(
        'properties',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('address_id', sa.Integer(), nullable=False),
        sa.Column('rooms', sa.Integer(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('price_per_night', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_properties_id'), 'properties', ['id'], unique=False)
    
    # Criar tabela reservations
    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('guests_quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.drop_table('reservations')
    op.drop_index(op.f('ix_properties_id'), table_name='properties')
    op.drop_table('properties')
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    op.drop_index(op.f('ix_clients_email'), table_name='clients')
    op.drop_table('clients')
    op.drop_index(op.f('ix_addresses_id'), table_name='addresses')
    op.drop_table('addresses')
