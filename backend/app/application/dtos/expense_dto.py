"""
2. ¿Estoy ejecutando una acción del sistema? → Estás en application/
•   ¿Estoy creando un caso de uso como CrearUsuario, ProcesarPago, ActualizarPerfil?
• 	¿Estoy orquestando entidades para cumplir una tarea?
• 	¿Estoy definiendo qué pasa cuando alguien hace una solicitud?
"""
# =============================================================================
# PASO 1: DTOs (Data Transfer Objects)
# =============================================================================

# app/application/dtos/expense_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ...domain.entities.expense import PaymentMethod

@dataclass
class CreateExpenseDTO:
    """
    DTO para crear un gasto
    Los DTO son onjetos simpres para transferir datos entre capas.
    No tienen lógica del negocio, solo datos.
    """
    amount: float
    category: str
    payment_method: str # Recibirá como string, luego se convierte a Enum
    description: Optional[str] = None
    date: Optional[datetime] = None
    
    def to_payment_method_enum(self) -> PaymentMethod:
        """Convierte el string a enum PaymentMethod"""
        return PaymentMethod(self.payment_method)
    
@dataclass
class UpdateExpenseDTO:
    """DTO para actualizar gasto"""
    expense_id: int
    amount: Optional[float] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None

    def to_payment_method_enum(self) -> Optional[PaymentMethod]:
        """Convierte el String a enum si existe"""
        if self.payment_method:
            return PaymentMethod(self.payment_method)
        return None


@dataclass
class ExpenseFilterDTO:
    """DTO para filtrar gastos"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None

@dataclass
class ExpenseResponseDTO:
    """
    DTO para responder con datos de un gasto
    Util para serializar a JSON en la API
    """
    id: int
    amount: float
    category: str
    payment_method: str
    date: str #ISO format
    description: Optional[str]
    formatted_amount: str
    is_recent: bool