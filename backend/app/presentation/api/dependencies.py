# =============================================================================
# PASO 2: DEPENDENCIES (Inyección de dependencias)
# =============================================================================

# app/presentation/api/dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from ...infrastructure.database.connection import get_db
from ...infrastructure.repositories.postgresql_expense_repository import PostgreSQLExpenseRepository
from ...application.use_cases.create_expense import CreateExpenseUseCase
from ...infrastructure.repositories.json_expense_repository import JsonExpenseRepository
from ...application.use_cases.create_expense import CreateExpenseUseCase
from ...application.use_cases.get_expense_by_id import GetExpenseByIdUseCase
from ...application.use_cases.get_all_expenses import GetAllExpensesUseCase
from ...application.use_cases.get_filtered_expenses import GetFilteredExpensesUseCase
from ...application.use_cases.update_expense import UpdateExpenseUseCase
from ...application.use_cases.delete_expense import DeleteExpenseUseCase
from ...application.use_cases.get_dashboard_data import GetDashboardDataUseCase
from ...core.config import settings

"""
def get_expense_repository() -> JsonExpenseRepository:
    
    #Dependency: Provee una instancia del repository
    
    #Aquí es donde se decide QUÉ implementación usar.
    #En el futuro puedes cambiar a PostgreSQL sin tocar nada más.
    
    settings.ensure_data_directory()
    return JsonExpenseRepository(settings.data_file_path)
"""

def get_expense_repository(
        db: Session = Depends(get_db)
)->PostgreSQLExpenseRepository:
    """
    Dependency: Provee una instancia del repository PostgreSQL
    
    ANTES: JsonExpenseRepository
    AHORA: PostgreSQLExpenseRepository
    """
    return PostgreSQLExpenseRepository(db)


def get_create_expense_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> CreateExpenseUseCase:
    """Dependency: Provee el caso de uso para crear gastos"""
    return CreateExpenseUseCase(repository)


def get_get_expense_by_id_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> GetExpenseByIdUseCase:
    """Dependency: Provee el caso de uso para obtener gasto por ID"""
    return GetExpenseByIdUseCase(repository)


def get_get_all_expenses_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> GetAllExpensesUseCase:
    """Dependency: Provee el caso de uso para obtener todos los gastos"""
    return GetAllExpensesUseCase(repository)


def get_get_filtered_expenses_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> GetFilteredExpensesUseCase:
    """Dependency: Provee el caso de uso para filtrar gastos"""
    return GetFilteredExpensesUseCase(repository)


def get_update_expense_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> UpdateExpenseUseCase:
    """Dependency: Provee el caso de uso para actualizar gastos"""
    return UpdateExpenseUseCase(repository)


def get_delete_expense_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> DeleteExpenseUseCase:
    """Dependency: Provee el caso de uso para eliminar gastos"""
    return DeleteExpenseUseCase(repository)


def get_get_dashboard_data_use_case(
    repository: Annotated[JsonExpenseRepository, Depends(get_expense_repository)]
) -> GetDashboardDataUseCase:
    """Dependency: Provee el caso de uso para obtener datos del dashboard"""
    return GetDashboardDataUseCase(repository)

