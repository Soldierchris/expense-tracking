# =============================================================================
# PASO 4: MAIN APP
# =============================================================================
# app/presentation/api/main.py - ACTUALIZADO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .expense_routes import router as expense_router, dashboard_router
from ...core.config import settings
from ...infrastructure.database.connection import init_db  # NUEVO

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para control de gastos personales con PostgreSQL",
    docs_url="/docs",
    redoc_url="/redoc"
)

# NUEVO: Inicializar BD al arrancar
@app.on_event("startup")
async def startup_event():
    """Evento de inicio: crear tablas si no existen"""
    init_db()
    print("✅ Base de datos PostgreSQL inicializada")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(expense_router)
app.include_router(dashboard_router)


@app.get("/", tags=["health"])
async def root():
    """Endpoint raíz - Health check"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "database": "PostgreSQL",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.presentation.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )