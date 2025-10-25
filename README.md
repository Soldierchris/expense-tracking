# =============================================================================
# README.md - Documentación del backend
# =============================================================================
# Guardar como: backend/README.md

"""
# Expense Tracker - Backend

Backend desarrollado con **Clean Architecture** usando Python y FastAPI.

## 🏗️ Arquitectura

```
app/
├── domain/          # Lógica de negocio pura
├── application/     # Casos de uso
├── infrastructure/  # Implementaciones técnicas
└── presentation/    # API REST
```

## 🚀 Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo .env
cp .env.example .env
```

## 🏃 Ejecutar

```bash
# Desarrollo
uvicorn app.presentation.api.main:app --reload

# La API estará disponible en: http://localhost:8000
# Documentación Swagger: http://localhost:8000/docs
```

## 🧪 Testing

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app
```

## 📁 Estructura del Proyecto

- **domain/**: Entidades y lógica de negocio
- **application/**: Casos de uso y DTOs
- **infrastructure/**: Repositorios y BD
- **presentation/**: API endpoints y schemas

## 🛠️ Tecnologías

- Python 3.11+
- FastAPI
- Pydantic
- Pytest
- JSON (storage)

## 📝 API Endpoints

- `POST /expenses/` - Crear gasto
- `GET /expenses/` - Listar gastos
- `GET /expenses/{id}` - Obtener gasto
- `PUT /expenses/{id}` - Actualizar gasto
- `DELETE /expenses/{id}` - Eliminar gasto
- `GET /dashboard/` - Datos del dashboard
"""
    