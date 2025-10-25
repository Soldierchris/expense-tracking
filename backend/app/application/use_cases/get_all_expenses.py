# app/application/use_cases/get_all_expenses.py
from typing import List
from ...domain.entities.expense import Expense
from ...domain.repositories.expense_repository import ExpenseRepository

class GetAllExpensesUseCase:
    """
    Caso de uso: Obtener todos los gastos
    """

    def __init__(self, expense_repository: ExpenseRepository):
        self._expense_repository = expense_repository
    
    def execute(self) -> List[Expense]:
        """
        Obtiene todos los gastos
        Returns: List[Expense]: Lista de todos los gastos
        """
        return self._expense_repository.get_all()
    