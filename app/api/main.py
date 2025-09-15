"""Aplicação principal FastAPI."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.routes import properties, reservations


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    # Sistema de Reservas de Propriedades

    API para gerenciamento de propriedades e reservas para estadias de curto e médio prazo.

    ## Funcionalidades

    ### 🏠 Propriedades
    - **Criar propriedade**: Cadastrar nova propriedade com endereço completo
    - **Listar propriedades**: Buscar com filtros por localização, capacidade e preço
    - **Verificar disponibilidade**: Checar disponibilidade para datas específicas

    ### 📅 Reservas
    - **Criar reserva**: Fazer reserva com validações automáticas
    - **Listar reservas**: Buscar por cliente ou propriedade
    - **Cancelar reserva**: Cancelamento seguro (soft delete)

    ## Validações Automáticas

    - **Datas**: Data fim > data início, sem datas passadas
    - **Disponibilidade**: Verificação de conflitos de reservas
    - **Capacidade**: Validação de limite de hóspedes
    - **Preço**: Cálculo automático (dias × preço_noite)

    ## Arquitetura

    Desenvolvido com **Arquitetura Hexagonal** (Ports & Adapters):
    - **Camada de Domínio**: Entidades puras
    - **Camada de Aplicação**: Use cases e DTOs
    - **Camada de Infraestrutura**: Repositórios e banco de dados
    - **Camada de Interface**: API FastAPI

    ## Tecnologias

    - **FastAPI** + **Python 3.10+**
    - **PostgreSQL** + **SQLAlchemy**
    - **Pydantic** para validação
    - **Alembic** para migrations
    """,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Handler global para exceções
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handler personalizado para HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handler para exceções não capturadas."""
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Erro interno do servidor",
            "status_code": 500
        }
    )


# Incluir roteadores
app.include_router(properties.router, prefix="/api/v1")
app.include_router(reservations.router, prefix="/api/v1")


# Rota de health check
@app.get("/", tags=["Health"])
async def root():
    """
    Health check da aplicação.
    
    Retorna informações básicas sobre o status da API.
    """
    return {
        "message": "Seazone API - Sistema de Reservas",
        "version": settings.app_version,
        "status": "healthy",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de health check para monitoramento.
    
    Útil para verificações de saúde da aplicação em ambientes de produção.
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
        "app": settings.app_name
    }


# Eventos de inicialização e shutdown
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação."""
    print(f"🚀 {settings.app_name} v{settings.app_version} iniciado!")
    print(f"📚 Documentação disponível em: http://{settings.host}:{settings.port}/docs")
    print(f"🔍 ReDoc disponível em: http://{settings.host}:{settings.port}/redoc")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado no shutdown da aplicação."""
    print(f"🛑 {settings.app_name} sendo finalizado...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )