# app/application/use_cases/get_filtered_expenses.py
from typing import List
from datetime import datetime
from ..dtos.expense_dto import ExpenseFilterDTO
from ...domain.entities.expense import Expense, PaymentMethod
from ...domain.repositories.expense_repository import ExpenseRepository

class GetFilteredExpensesUseCase:
    """
    Caso de uso: Obtener gastos con filtros
    Permite combinar multiples filtros
    """

    def __init__(self, expense_repository: ExpenseRepository):
        self._expense_respository = expense_repository


    #def execute(self, filters: ExpenseFilterDTO) -> List[Expense]:
    def execute(self, filters: ExpenseFilterDTO) -> List[Expense]:
     
         
         #Obtiene gastos apliando filtros
         #Args: Filtros a aplicar
         #Returns: List[Expense]: Lista de gastos filtrados
             
        
        #1. Filtrar por rango de fechas si existe
        if filters.start_date and filters.end.date:
            expenses = self._expense_repository.get_by_date_range(
                 filters.start_date,
                 filters.end_date
                 
            )
        else:
            expenses=self._expense_repository.get_all()

        # 2. Aplicar filtros adicionales en memoria
        if filters.category:
            expenses = [ e for e in expenses
                        if e.category.lower() == filters.category.lower()]
                    
        
        if filters.payment_method:
            payment_enum = PaymentMethod(filters.payment_method)
            expenses = [e for e in expenses
                        if e.payment_method == payment_enum]
            

        if filters.min_amount is not None:
            expenses = [e for e in expenses
                        if e.amount>=filters.min_amount]
            

        if filters.max_amount is not None:
            expenses = [e for e in expenses
                        if e.amount <= filters.max_amount]
            

        return expenses