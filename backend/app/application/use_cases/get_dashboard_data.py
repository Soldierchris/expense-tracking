# app/application/use_cases/get_dashboard_data.py
from typing import Dict, List
from datetime import datetime, timedelta
from ...domain.repositories.expense_repository import ExpenseRepository
from ...domain.services.expense_service import ExpenseService


class GetDashboardDataUseCase:
    """
    Caso de uso: Obtener datos para el dashboard
    
    Orquesta múltiples operaciones:
    - Gastos recientes
    - Totales por categoría
    - Totales por método de pago
    - Resumen y estadísticas
    """
    
    def __init__(self, expense_repository: ExpenseRepository):
        self._expense_repository = expense_repository
        self._expense_service = ExpenseService()
    
    def execute(self, days: int = 30) -> Dict:
        """
        Obtiene todos los datos del dashboard
        
        Args:
            days: Número de días a considerar
            
        Returns:
            Dict: Datos completos del dashboard
        """
        # 1. Obtener gastos recientes
        recent_expenses = self._expense_repository.get_recent_expenses(days)
        
        # 2. Obtener todos los gastos para comparación
        all_expenses = self._expense_repository.get_all()
        
        # 3. Calcular métricas usando el service
        monthly_summary = self._expense_service.calculate_monthly_summary(recent_expenses)
        spending_trend = self._expense_service.get_spending_trend(all_expenses, days)
        
        # 4. Obtener totales agregados
        category_totals = self._expense_repository.get_total_by_category()
        payment_totals = self._expense_repository.get_total_by_payment_method()
        category_counts = self._expense_repository.get_count_by_category()
        
        # 5. Preparar respuesta completa
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        dashboard_data = {
            "period_info": {
                "days": days,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "summary": {
                "total_amount": monthly_summary.get("total", 0),
                "expense_count": monthly_summary.get("expense_count", 0),
                "average_per_expense": (
                    monthly_summary.get("total", 0) / monthly_summary.get("expense_count", 1)
                    if monthly_summary.get("expense_count", 0) > 0 else 0
                )
            },
            "by_category": {
                "totals": category_totals,
                "counts": category_counts
            },
            "by_payment_method": payment_totals,
            "trend": spending_trend,
            "recent_expenses": [
                {
                    "id": expense.id,
                    "amount": expense.amount,
                    "formatted_amount": expense.get_formatted_amount(),
                    "category": expense.category,
                    "payment_method": expense.payment_method.value,
                    "date": expense.date.isoformat(),
                    "description": expense.description,
                    "is_recent": expense.is_recent(7)
                }
                for expense in sorted(recent_expenses, key=lambda x: x.date, reverse=True)[:10]
            ]
        }
        
        return dashboard_data
