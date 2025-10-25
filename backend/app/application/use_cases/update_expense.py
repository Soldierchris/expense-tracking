# app/application/use_cases/update_expense.py
from ..dtos.expense_dto import UpdateExpenseDTO
from ...domain.entities.expense import Expense
from ...domain.repositories.expense_repository import ExpenseRepository
from ...domain.repositories.exceptions import ExpenseNotFoundError

class UpdateExpenseUseCase:
    """
    Caso de uso: ACtualizar un gasto existente
    """

    def __init__ (self, expense_respository: ExpenseRepository ):
        self._expense_repository=expense_respository
    
    def execute(self, update_dto: UpdateExpenseDTO) -> Expense:
        """
        Actauliza un gasto existente
        Args: update_dto: Datos a actualizar
        Returns: Expense: El gasto actualizado
        Raises: ExpenseNotFoundError: Si el gasto no existe
        """

        # 1. Obtener el gasto existente
        existing_expense = self._expense_repository.get_by_id(update_dto.expense_id)

        # 2. Aplicar cambios usando métodos de la entidad
        if update_dto.amount is not None:
            existing_expense.update_amount(update_dto.amount)

        if update_dto.category is not None:
            existing_expense.update_category(update_dto.category)

        if update_dto.payment_method is not None:
            existing_expense.payment_method= update_dto.to_payment_method_enum()

        if update_dto.description is not None:
            existing_expense.description = update_dto.description.strip() if update_dto.description else None
        
        # 3. Guardar cambios
        updated_expense =  self._expense_repository.update(existing_expense)

        return updated_expense

    
