# app/application/use_cases/create_expense.py

from typing import Optional
from ..dtos.expense_dto import CreateExpenseDTO
from ...domain.entities.expense import Expense
from ...domain.repositories.expense_repository import ExpenseRepository

class CreateExpenseUseCase:
    """
    Caso de uso: Crear un nuevo gasto

    Responsabilidades:
    1. Validar datos de entrada (DTO) 
    2. Crear la entidad Expsense (con sus validaciones)
    3. Guardar usando el repository
    4. Retornar el gasti creado
    """

    def __init__ (self, expense_repository: ExpenseRepository):
        """
        Inicializar el caso de uso con sus dependencias
        Args: expense_repository: Repository para persistir gastos
        """
        self._expense_repository = expense_repository

    def execute(self, create_expense_dto: CreateExpenseDTO) -> Expense:
        """
        Ejecuta el caso de uso de crear gasto
        Args: create_expense_dto: Datos del gasto a crear
        Returns: Expense: El gasto creado con ID asignado
        Raises: ValueError: Si los datos son invalidos
        """
        # 1. Convertir DTO a entidad (aquí se ejecutan las validaciones)
        expense = Expense(
            amount=create_expense_dto.amount,
            category=create_expense_dto.category,
            payment_method=create_expense_dto.to_payment_method_enum(),
            description=create_expense_dto.description,
            date=create_expense_dto.date
        )

        #Guardar usando el repositorio
        saved_expense = self._expense_repository.save(expense)
        return saved_expense
    

    