# Seazone API - Sistema de Reservas


## Arquitetura

**Arquitetura Hexagonal (Ports & Adapters)** com separação clara de responsabilidades

### Padrões Implementados
- **Repository Pattern** para isolamento de dados
- **DTOs** para validação e transferência de dados
- **Dependency Injection** para inversão de controle
- **Use Cases** para lógica de negócio

## Setup projeto

### 1. Clonar o repositório
```bash
git clone <repository-url>
cd seazone-api
```

### 2. Configurar ambiente Python
```bash
python -m venv .venv

source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env

# Editar variáveis (se precisar)
nano .env
```

### 4. Executar aplicação

### 4.1 Banco de dados em Docker + Aplicação sem Docker
```bash
# Iniciar PostgreSQL
docker-compose --env-file .env up --build postgres   

# Aplicar migrations (necessário estar utilizando ambiente virtual - conforme passo 2)
alembic upgrade head

# Iniciar aplicação python
uvicorn app.api.main:app --reload
```

### 4.1 Banco de dados e Aplicação em Docker
```bash
# Docker Compose (Iniciar aplicação + PostgreSQL)
docker-compose --env-file .env up --build

# Aplicar migrations (necessário estar utilizando ambiente virtual - conforme passo 2)
alembic upgrade head
```

## Uso da API

A API está disponível em `http://localhost:8000` após inicializar a aplicação.

## Documentação da API

A documentação interativa completa está disponível em:

- **Swagger**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`