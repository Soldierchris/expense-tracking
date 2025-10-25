# =============================================================================
# app/core/config.py - Configuración centralizada
# =============================================================================
# Guardar como: backend/app/core/config.py

from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuración de la aplicación
    
    Lee las variables de entorno del archivo .env
    """
    
    # Información de la aplicación
    app_name: str = "Expense Tracker"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Configuración de archivos
    data_file_path: str = "data/expenses.json"
    
    # Configuración de API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Database (futuro)
    # database_url: str = "sqlite:///./expenses.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_cors_origins(self) -> List[str]:
        """Convierte el string de orígenes a lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    def ensure_data_directory(self) -> None:
        """Crea el directorio de datos si no existe"""
        data_path = Path(self.data_file_path)
        data_path.parent.mkdir(parents=True, exist_ok=True)


# Instancia global de configuración
settings = Settings()