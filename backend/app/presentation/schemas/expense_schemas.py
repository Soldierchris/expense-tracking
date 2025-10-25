# =============================================================================
# PASO 1: SCHEMAS (Validación con Pydantic)
# =============================================================================

# app/presentation/schemas/expense_schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ExpenseCreateSchema(BaseModel):
    """
    Schema para crear un gasto
    Valida los datos que vienen desde el frontend
    """
    amount: float = Field(..., gt=0, description="Monto del gasto (debe ser mayor a 0)")
    category: str = Field(..., min_length=1, max_length=100, description="Categoría del gasto")
    payment_method: str = Field(..., description="Método de pago: cash, debit_card, credit_card")
    description: Optional[str] = Field(None, max_length=500, description="Descripción opcional")
    date: Optional[datetime] = Field(None, description="Fecha del gasto (por defecto: ahora)")
    
    @field_validator('payment_method')
    @classmethod
    def validate_payment_method(cls, v: str) -> str:
        """Valida que el método de pago sea válido"""
        allowed = ['cash', 'debit_card', 'credit_card']
        if v not in allowed:
            raise ValueError(f'Método de pago debe ser uno de: {", ".join(allowed)}')
        return v
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Valida que la categoría no esté vacía"""
        if not v or v.strip() == "":
            raise ValueError('La categoría no puede estar vacía')
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": 25.50,
                    "category": "Comida",
                    "payment_method": "cash",
                    "description": "Almuerzo en restaurante",
                    "date": "2024-01-15T12:30:00"
                }
            ]
        }
    }


class ExpenseUpdateSchema(BaseModel):
    """Schema para actualizar un gasto"""
    amount: Optional[float] = Field(None, gt=0, description="Nuevo monto")
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    payment_method: Optional[str] = Field(None)
    description: Optional[str] = Field(None, max_length=500)
    
    @field_validator('payment_method')
    @classmethod
    def validate_payment_method(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed = ['cash', 'debit_card', 'credit_card']
            if v not in allowed:
                raise ValueError(f'Método de pago debe ser uno de: {", ".join(allowed)}')
        return v


class ExpenseResponseSchema(BaseModel):
    """Schema para responder con un gasto"""
    id: int
    amount: float
    category: str
    payment_method: str
    date: datetime
    description: Optional[str]
    formatted_amount: str
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "amount": 25.50,
                    "category": "Comida",
                    "payment_method": "cash",
                    "date": "2024-01-15T12:30:00",
                    "description": "Almuerzo",
                    "formatted_amount": "$25.50"
                }
            ]
        }
    }


class ExpenseListResponseSchema(BaseModel):
    """Schema para lista de gastos"""
    expenses: list[ExpenseResponseSchema]
    total: int
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "expenses": [],
                    "total": 0
                }
            ]
        }
    }


class DashboardResponseSchema(BaseModel):
    """Schema para respuesta del dashboard"""
    period_info: dict
    summary: dict
    by_category: dict
    by_payment_method: dict
    trend: dict
    recent_expenses: list[dict]


class ErrorResponseSchema(BaseModel):
    """Schema para respuestas de error"""
    detail: str
    error_code: Optional[str] = None