
# =============================================================================
# PASO 3: DOMAIN SERVICE (actualización)
# =============================================================================

# app/domain/services/expense_service.py
from typing import List, Dict
from datetime import datetime, timedelta
from ..entities.expense import Expense


class ExpenseService:
    """
    Servicios del dominio - Lógica compleja que no pertenece a una entidad
    """
    
    @staticmethod
    def calculate_monthly_summary(expenses: List[Expense]) -> Dict:
        """
        Calcula resumen de gastos
        
        Args:
            expenses: Lista de gastos
            
        Returns:
            Dict: Resumen con totales y conteos
        """
        if not expenses:
            return {
                "total": 0,
                "by_category": {},
                "by_payment_method": {},
                "expense_count": 0
            }
        
        total = sum(expense.amount for expense in expenses)
        
        by_category = {}
        by_payment_method = {}
        
        for expense in expenses:
            # Por categoría
            if expense.category not in by_category:
                by_category[expense.category] = 0
            by_category[expense.category] += expense.amount
            
            # Por método de pago
            method = expense.payment_method.value
            if method not in by_payment_method:
                by_payment_method[method] = 0
            by_payment_method[method] += expense.amount
        
        return {
            "total": total,
            "by_category": by_category,
            "by_payment_method": by_payment_method,
            "expense_count": len(expenses)
        }
    
    @staticmethod
    def get_spending_trend(expenses: List[Expense], days: int = 30) -> Dict:
        """
        Analiza tendencia de gastos
        
        Args:
            expenses: Lista de gastos
            days: Número de días a analizar
            
        Returns:
            Dict: Análisis de tendencia
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_expenses = [e for e in expenses if e.date >= cutoff_date]
        
        if not recent_expenses:
            return {
                "total_period": 0,
                "average_daily": 0,
                "expense_count": 0
            }
        
        total = sum(e.amount for e in recent_expenses)
        
        return {
            "total_period": total,
            "average_daily": total / days,
            "expense_count": len(recent_expenses)
        }