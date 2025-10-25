#app/application/use_cases/delete_expense.py
from ...domain.repositories.expense_repository import ExpenseRepository

class DeleteExpenseUseCase:
    """
    Caso de uso: Eliminar un gasto
    """

    def __init__(self, expense_repository: ExpenseRepository):
        self._expense_repository = expense_repository

    def execute(self, expense_id: int) -> bool:
        """
        Elimina un gasto por ID
        Args: expense_id: ID del gasto a eliminar
        Returns: bool: True si se elimono, False si no existia
        """
        return self._expense_repository.delete(expense_id)
        