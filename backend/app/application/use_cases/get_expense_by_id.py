# app/application/use_cases/get_expense_by_id.py

from typing import Optional
from ...domain.entities.expense import Expense
from ...domain.repositories.expense_repository import ExpenseRepository
from ...domain.repositories.exceptions import ExpenseNotFoundError

class GetExpenseByIdUseCase:
    """
    Caso de uso: Obtener un gasto por ID
    """

    def __init__(self, expense_repository: ExpenseRepository):
        self._expense_repository = expense_repository
        
    def execute(self, expense_id: int) -> Expense:
        """
        Obtiene un gasto por ID
        Args: expense_id: ID del gasto a buscar
        Returns: Expense: El gasto encontrado 
        Raises: ExpenseNotFOund: Si no se encuentra el gasto
        """
        expense = self._expense_repository.get_by_id(expense_id)
        
        if expense is None:
            raise ExpenseNotFoundError(expense_id)
        return expense
        