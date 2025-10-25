# =============================================================================
# 5. POSTGRESQL REPOSITORY IMPLEMENTATION
# =============================================================================

# app/infrastructure/repositories/postgresql_expense_repository.py

from typing import List,Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from ...domain.entities.expense import Expense, PaymentMethod
from ...domain.repositories.expense_repository import ExpenseRepository
from ...domain.repositories.exceptions import (
    ExpenseNotFoundError, RepositoryError
)

from ..database.models import ExpenseModel, PaymentMethodEnum


class PostgreSQLExpenseRepository(ExpenseRepository):
    """
    Implementación de ExpenseRepository
    Esta es la implementacion REAL para produccion
    USA SQLAlchemy para comunicarse con PostgreeSQL
    """
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesion de BD
        Args: Sesion de SQLAlchemy
        """
        self.db = db
        
    def model_to_entity(self, model: ExpenseModel) -> Expense:
        """
        Convierte un modelo se SQLALchemy a una entidad de dominio
        Args: model: Modelo de SQLAlchemy
        Returns: Expense: Entidad del dominio
        """
        return Expense(
            amount=model.amount,
            category=model.category,
            payment_method=PaymentMethod(model.payment_method.value),
            date=model.date,
            description=model.description,
            id=model.id
        )
    
    def save(self, expense: Expense)->Expense:
        """Guarda un gasto nuevo"""
        try:
            model= self._entity_to_model(expense)
            # Si tiene ID, es actualizacion
            if model.id:
                model.id = None # SQLAlchemy  asiginara nuevo ID

            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

            return self._model_to_entity(model)
        
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Error al guardar gasto:{str(e)}")
        

    def get_by_id(self, expense_id:int ) -> Optional[Expense]:
        """Obtiene un gasto por ID"""
        model = self.db.query(ExpenseModel).filter(
            ExpenseModel.id==expense_id
        ).first()

        if not model:
            return None
        return self._model_to_entity(model)

    def get_all(self)-> List[Expense]:
        """Obtiene todos los gastos"""
        models = self.db.query(ExpenseModel).order_by(
            ExpenseModel.date.desc()
        ).all    
        return [self._model_to_entity(model)for model in models]
    
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    )->List[Expense]:
        """Obtiene los gastos en un rango de fechas"""
        models = self.db.query(ExpenseModel).filter(
            ExpenseModel.date >= start_date,
            ExpenseModel.date <= end_date
        ).order_by(ExpenseModel.date.desc()).all()

        return[self._model_to_entity(model) for model in models]
    
    def get_by_category(self, category:str)->List[Expense]:
        """Obtiene gastos de una categoria"""
        models = self.db.query(ExpenseModel).filter(
            func.lower(ExpenseModel.category) == category.lower()
        ).order_by(ExpenseModel.date.desc()).all()

        return [self._model_to_entity(model) for model in models]

