# =============================================================================
# PASO 3: ROUTES/ENDPOINTS
# =============================================================================

# app/presentation/api/expense_routes.py
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime

from ..schemas.expense_schemas import (
    ExpenseCreateSchema,
    ExpenseUpdateSchema,
    ExpenseResponseSchema,
    ExpenseListResponseSchema,
    DashboardResponseSchema,
    ErrorResponseSchema
)
from .dependencies import (
    get_create_expense_use_case,
    get_get_expense_by_id_use_case,
    get_get_all_expenses_use_case,
    get_get_filtered_expenses_use_case,
    get_update_expense_use_case,
    get_delete_expense_use_case,
    get_get_dashboard_data_use_case
)
from ...application.use_cases.create_expense import CreateExpenseUseCase
from ...application.use_cases.get_expense_by_id import GetExpenseByIdUseCase
from ...application.use_cases.get_all_expenses import GetAllExpensesUseCase
from ...application.use_cases.get_filtered_expenses import GetFilteredExpensesUseCase
from ...application.use_cases.update_expense import UpdateExpenseUseCase
from ...application.use_cases.delete_expense import DeleteExpenseUseCase
from ...application.use_cases.get_dashboard_data import GetDashboardDataUseCase
from ...application.dtos.expense_dto import (
    CreateExpenseDTO,
    UpdateExpenseDTO,
    ExpenseFilterDTO
)
from ...domain.repositories.exceptions import ExpenseNotFoundError


router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post(
    "/",
    response_model=ExpenseResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo gasto",
    responses={
        201: {"description": "Gasto creado exitosamente"},
        400: {"model": ErrorResponseSchema, "description": "Datos inválidos"},
        500: {"model": ErrorResponseSchema, "description": "Error interno"}
    }
)
async def create_expense(
    expense_data: ExpenseCreateSchema,
    use_case: Annotated[CreateExpenseUseCase, Depends(get_create_expense_use_case)]
):
    """
    Crea un nuevo gasto.
    
    - **amount**: Monto del gasto (debe ser mayor a 0)
    - **category**: Categoría del gasto
    - **payment_method**: cash, debit_card, o credit_card
    - **description**: Descripción opcional
    - **date**: Fecha del gasto (opcional, por defecto: ahora)
    """
    try:
        # Convertir schema a DTO
        dto = CreateExpenseDTO(
            amount=expense_data.amount,
            category=expense_data.category,
            payment_method=expense_data.payment_method,
            description=expense_data.description,
            date=expense_data.date
        )
        
        # Ejecutar caso de uso
        expense = use_case.execute(dto)
        
        # Convertir entidad a schema de respuesta
        return ExpenseResponseSchema(
            id=expense.id,
            amount=expense.amount,
            category=expense.category,
            payment_method=expense.payment_method.value,
            date=expense.date,
            description=expense.description,
            formatted_amount=expense.get_formatted_amount()
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear gasto: {str(e)}"
        )


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponseSchema,
    summary="Obtener un gasto por ID",
    responses={
        200: {"description": "Gasto encontrado"},
        404: {"model": ErrorResponseSchema, "description": "Gasto no encontrado"}
    }
)
async def get_expense(
    expense_id: int,
    use_case: Annotated[GetExpenseByIdUseCase, Depends(get_get_expense_by_id_use_case)]
):
    """Obtiene un gasto específico por su ID."""
    try:
        expense = use_case.execute(expense_id)
        
        return ExpenseResponseSchema(
            id=expense.id,
            amount=expense.amount,
            category=expense.category,
            payment_method=expense.payment_method.value,
            date=expense.date,
            description=expense.description,
            formatted_amount=expense.get_formatted_amount()
        )
    
    except ExpenseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=ExpenseListResponseSchema,
    summary="Listar todos los gastos o filtrar",
    responses={
        200: {"description": "Lista de gastos"}
    }
)
async def list_expenses(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    payment_method: Optional[str] = Query(None, description="Filtrar por método de pago"),
    min_amount: Optional[float] = Query(None, description="Monto mínimo"),
    max_amount: Optional[float] = Query(None, description="Monto máximo"),
    use_case_all: Annotated[GetAllExpensesUseCase, Depends(get_get_all_expenses_use_case)] = None,
    use_case_filtered: Annotated[GetFilteredExpensesUseCase, Depends(get_get_filtered_expenses_use_case)] = None
):
    """
    Lista todos los gastos o aplica filtros opcionales.
    
    Filtros disponibles:
    - **category**: Filtrar por categoría
    - **payment_method**: cash, debit_card, credit_card
    - **min_amount**: Monto mínimo
    - **max_amount**: Monto máximo
    """
    try:
        # Si hay filtros, usar caso de uso de filtrado
        if any([category, payment_method, min_amount, max_amount]):
            filters = ExpenseFilterDTO(
                category=category,
                payment_method=payment_method,
                min_amount=min_amount,
                max_amount=max_amount
            )
            expenses = use_case_filtered.execute(filters)
        else:
            # Si no hay filtros, obtener todos
            expenses = use_case_all.execute()
        
        # Convertir entidades a schemas
        expense_responses = [
            ExpenseResponseSchema(
                id=expense.id,
                amount=expense.amount,
                category=expense.category,
                payment_method=expense.payment_method.value,
                date=expense.date,
                description=expense.description,
                formatted_amount=expense.get_formatted_amount()
            )
            for expense in expenses
        ]
        
        return ExpenseListResponseSchema(
            expenses=expense_responses,
            total=len(expense_responses)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar gastos: {str(e)}"
        )


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponseSchema,
    summary="Actualizar un gasto",
    responses={
        200: {"description": "Gasto actualizado"},
        404: {"model": ErrorResponseSchema, "description": "Gasto no encontrado"},
        400: {"model": ErrorResponseSchema, "description": "Datos inválidos"}
    }
)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdateSchema,
    use_case: Annotated[UpdateExpenseUseCase, Depends(get_update_expense_use_case)]
):
    """Actualiza un gasto existente."""
    try:
        dto = UpdateExpenseDTO(
            expense_id=expense_id,
            amount=expense_data.amount,
            category=expense_data.category,
            payment_method=expense_data.payment_method,
            description=expense_data.description
        )
        
        expense = use_case.execute(dto)
        
        return ExpenseResponseSchema(
            id=expense.id,
            amount=expense.amount,
            category=expense.category,
            payment_method=expense.payment_method.value,
            date=expense.date,
            description=expense.description,
            formatted_amount=expense.get_formatted_amount()
        )
    
    except ExpenseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un gasto",
    responses={
        204: {"description": "Gasto eliminado exitosamente"},
        404: {"model": ErrorResponseSchema, "description": "Gasto no encontrado"}
    }
)
async def delete_expense(
    expense_id: int,
    use_case: Annotated[DeleteExpenseUseCase, Depends(get_delete_expense_use_case)]
):
    """Elimina un gasto por ID."""
    result = use_case.execute(expense_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gasto con ID {expense_id} no encontrado"
        )
    
    return None  # 204 No Content


# Router para dashboard
dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@dashboard_router.get(
    "/",
    response_model=DashboardResponseSchema,
    summary="Obtener datos del dashboard",
    responses={
        200: {"description": "Datos del dashboard"}
    }
)
async def get_dashboard(
    days: int = Query(30, description="Número de días a considerar", ge=1, le=365),
    use_case: Annotated[GetDashboardDataUseCase, Depends(get_get_dashboard_data_use_case)] = None
):
    """
    Obtiene todos los datos para el dashboard.
    
    Incluye:
    - Resumen del período
    - Totales por categoría
    - Totales por método de pago
    - Tendencias de gasto
    - Gastos recientes
    """
    try:
        dashboard_data = use_case.execute(days=days)
        return dashboard_data
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener datos del dashboard: {str(e)}"
        )