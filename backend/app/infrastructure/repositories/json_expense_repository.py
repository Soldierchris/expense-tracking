# app/infrastructure/repositories/json_expense_repository.py
import json
import os
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path

from ...domain.entities.expense import Expense, PaymentMethod
from ...domain.repositories.expense_repository import ExpenseRepository
from ...domain.repositories.exceptions import (
    ExpenseNotFoundError, 
    RepositoryError,
    RepositoryConnectionError
)


class JsonExpenseRepository(ExpenseRepository):
    """
    Implementación del ExpenseRepository usando archivo JSON
    
    Esta clase implementa CÓMO guardar/recuperar gastos usando JSON.
    Es perfecta para:
    - Desarrollo rápido
    - Testing
    - Proyectos pequeños
    - No requiere base de datos instalada
    """
    
    def __init__(self, file_path: str = "expenses.json"):
        """
        Inicializa el repositorio JSON
        
        Args:
            file_path: Ruta del archivo JSON donde se guardarán los gastos
        """
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Crea el archivo JSON si no existe"""
        if not self.file_path.exists():
            self._save_to_file([])
    
    def _load_from_file(self) -> List[dict]:
        """
        Carga los datos del archivo JSON
        
        Returns:
            List[dict]: Lista de gastos en formato diccionario
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError as e:
            raise RepositoryError(f"Error al leer el archivo JSON: {e}")
        except Exception as e:
            raise RepositoryConnectionError(f"Error al acceder al archivo: {e}")
    
    def _save_to_file(self, data: List[dict]) -> None:
        """
        Guarda los datos en el archivo JSON
        
        Args:
            data: Lista de gastos en formato diccionario
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RepositoryConnectionError(f"Error al guardar en el archivo: {e}")
    
    def _dict_to_expense(self, data: dict) -> Expense:
        """
        Convierte un diccionario a una entidad Expense
        
        Args:
            data: Diccionario con datos del gasto
            
        Returns:
            Expense: Entidad creada
        """
        return Expense(
            amount=float(data['amount']),
            category=data['category'],
            payment_method=PaymentMethod(data['payment_method']),
            date=datetime.fromisoformat(data['date']) if data.get('date') else None,
            description=data.get('description'),
            id=data.get('id')
        )
    
    def _expense_to_dict(self, expense: Expense) -> dict:
        """
        Convierte una entidad Expense a diccionario
        
        Args:
            expense: Entidad a convertir
            
        Returns:
            dict: Diccionario con datos del gasto
        """
        return {
            'id': expense.id,
            'amount': expense.amount,
            'category': expense.category,
            'payment_method': expense.payment_method.value,
            'date': expense.date.isoformat() if expense.date else None,
            'description': expense.description
        }
    
    def _get_next_id(self) -> int:
        """
        Obtiene el próximo ID disponible
        
        Returns:
            int: Próximo ID a usar
        """
        data = self._load_from_file()
        if not data:
            return 1
        return max(item['id'] for item in data) + 1
    
    def save(self, expense: Expense) -> Expense:
        """
        Guarda un gasto nuevo
        """
        data = self._load_from_file()
        
        # Asignar ID si es nuevo
        if expense.id is None:
            expense.id = self._get_next_id()
        
        # Convertir a diccionario y agregar
        expense_dict = self._expense_to_dict(expense)
        data.append(expense_dict)
        
        # Guardar en archivo
        self._save_to_file(data)
        
        return expense
    
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        """
        Obtiene un gasto por ID
        """
        data = self._load_from_file()
        
        for item in data:
            if item.get('id') == expense_id:
                return self._dict_to_expense(item)
        
        return None
    
    def get_all(self) -> List[Expense]:
        """
        Obtiene todos los gastos
        """
        data = self._load_from_file()
        return [self._dict_to_expense(item) for item in data]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Expense]:
        """
        Obtiene gastos en un rango de fechas
        """
        all_expenses = self.get_all()
        
        return [
            expense for expense in all_expenses
            if start_date <= expense.date <= end_date
        ]
    
    def get_by_category(self, category: str) -> List[Expense]:
        """
        Obtiene gastos de una categoría específica
        """
        all_expenses = self.get_all()
        category_lower = category.lower()
        
        return [
            expense for expense in all_expenses
            if expense.category.lower() == category_lower
        ]
    
    def get_by_payment_method(self, payment_method: str) -> List[Expense]:
        """
        Obtiene gastos por método de pago
        """
        all_expenses = self.get_all()
        
        return [
            expense for expense in all_expenses
            if expense.payment_method.value == payment_method
        ]
    
    def update(self, expense: Expense) -> Expense:
        """
        Actualiza un gasto existente
        """
        if expense.id is None:
            raise RepositoryError("No se puede actualizar un gasto sin ID")
        
        data = self._load_from_file()
        
        # Buscar el índice del gasto
        index = None
        for i, item in enumerate(data):
            if item.get('id') == expense.id:
                index = i
                break
        
        if index is None:
            raise ExpenseNotFoundError(expense.id)
        
        # Actualizar el gasto
        data[index] = self._expense_to_dict(expense)
        self._save_to_file(data)
        
        return expense
    
    def delete(self, expense_id: int) -> bool:
        """
        Elimina un gasto por ID
        """
        data = self._load_from_file()
        
        # Filtrar para eliminar el gasto
        new_data = [item for item in data if item.get('id') != expense_id]
        
        # Si el tamaño cambió, se eliminó algo
        if len(new_data) < len(data):
            self._save_to_file(new_data)
            return True
        
        return False
    
    def get_total_by_category(self) -> Dict[str, float]:
        """
        Obtiene totales agrupados por categoría
        """
        all_expenses = self.get_all()
        totals: Dict[str, float] = {}
        
        for expense in all_expenses:
            if expense.category not in totals:
                totals[expense.category] = 0
            totals[expense.category] += expense.amount
        
        return totals
    
    def get_total_by_payment_method(self) -> Dict[str, float]:
        """
        Obtiene totales agrupados por método de pago
        """
        all_expenses = self.get_all()
        totals: Dict[str, float] = {}
        
        for expense in all_expenses:
            method = expense.payment_method.value
            if method not in totals:
                totals[method] = 0
            totals[method] += expense.amount
        
        return totals
    
    def get_count_by_category(self) -> Dict[str, int]:
        """
        Obtiene cantidad de gastos por categoría
        """
        all_expenses = self.get_all()
        counts: Dict[str, int] = {}
        
        for expense in all_expenses:
            if expense.category not in counts:
                counts[expense.category] = 0
            counts[expense.category] += 1
        
        return counts
    
    def search_by_description(self, search_term: str) -> List[Expense]:
        """
        Busca gastos por descripción (búsqueda parcial)
        """
        all_expenses = self.get_all()
        search_lower = search_term.lower()
        
        return [
            expense for expense in all_expenses
            if expense.description and search_lower in expense.description.lower()
        ]
    
    def get_recent_expenses(self, days: int = 30) -> List[Expense]:
        """
        Obtiene gastos de los últimos N días
        """
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.get_by_date_range(start_date, end_date)
    
    def clear_all(self) -> None:
        """
        Elimina todos los gastos (útil para testing)
        ⚠️ CUIDADO: Esta operación es irreversible
        """
        self._save_to_file([])
    
    def get_file_stats(self) -> Dict:
        """
        Obtiene estadísticas del archivo JSON
        Útil para debugging
        """
        data = self._load_from_file()
        
        return {
            'file_path': str(self.file_path),
            'file_exists': self.file_path.exists(),
            'total_expenses': len(data),
            'file_size_bytes': self.file_path.stat().st_size if self.file_path.exists() else 0
        }