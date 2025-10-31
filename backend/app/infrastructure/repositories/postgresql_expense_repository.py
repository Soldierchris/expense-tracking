# =============================================================================
# 5. POSTGRESQL REPOSITORY IMPLEMENTATION
# =============================================================================

# app/infrastructure/repositories/postgresql_expense_repository.py

from typing import List,Optional, Dict
from datetime import datetime
from datetime import timezone
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
        
    def _model_to_entity(self, model: ExpenseModel) -> Expense:
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
    
    def _entity_to_model(self, entity: Expense) -> ExpenseModel:
        """
        Convierte una entidad del dominio a un modelo de SQLAlchemy
        
        Args:
            entity: Entidad del dominio
            
        Returns:
            ExpenseModel: Modelo de SQLAlchemy
        """
        return ExpenseModel(
            id=entity.id,
            amount=entity.amount,
            category=entity.category,
            payment_method=PaymentMethodEnum(entity.payment_method.value),
            date=entity.date,
            description=entity.description
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


    def get_by_payment_method(self, payment_method: str) -> List[Expense]:
        """Obtiene Gastos por método de pago"""
        models = self.db.query(ExpenseModel).filter(
            ExpenseModel.payment_method == PaymentMethodEnum(payment_method)
        ).order_by(ExpenseModel.date.desc()).all()

        return[self._model_to_entity(model) for model in models]
    
    def update(self, expense: Expense) -> Expense:
        """Actualiza un gasto existente"""
        if not expense.id:
            raise RecursionError("No se puede actualizar un gasto sin ID")
    
        try:
            model = self.db.query(ExpenseModel).filter(
                ExpenseModel.id == expense.id
            ).first()

            if not model:
                raise ExpenseNotFoundError(expense.id)
            
            #Actualizar campos
            model.amount = expense.amount
            model.category = expense.category
            model.payment_method = PaymentMethodEnum(expense.payment_method.value)
            model.description = expense.description
            model.date = expense.date
            model.update_at = datetime.now(timezone.utc)

            self.db.commit()
            self.db.refresh(model)

            return self._model_to_entity(model)
        
        except ExpenseNotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Error al actualizar gasto: {str(e)}")
        
    def delete(self, expense_id: int) -> bool:
        """Elimina un gasto"""
        try:
            model = self.db.query(ExpenseModel).filter(
                ExpenseModel.id == expense_id
            ).first()

            if not model:
                return False
            
            self.db.delete(model)
            self.db.commit()

            return True
        except Exception as e:
            self.db.rollback()
            raise RepositoryError(f"Error al eliminar el gasto: {str(e)}")
        

    def get_total_by_category(self) -> Dict[str,float]:
        """Obtiene gastos totales agrupados por categoria"""
        results = self.db.query(
            ExpenseModel.category,
            func.sum(ExpenseModel.amount).label('total')
        ).group_by(ExpenseModel.category).all()

        return {category: float(total) for category, total in results}
    
    def get_total_by_payment_method(self) -> Dict[str,float]:
        """Obtiene los gastos agrupados por metodo de pago"""
        results = self.db.query(
            ExpenseModel.payment_method,
            func.sum(ExpenseModel.amount).label('total')
        ).group_by(ExpenseModel.payment_method).all()

        return {method.value: float(total) for method, total in results}
    
    def get_count_by_category(self) -> Dict[str,int]:
        """Obtiene la cantidad de gastos por categoria"""
        results = self.db.query(
            ExpenseModel.category,
            func.count(ExpenseModel.id).label('count')
        )
        return {category: count for category, count in results}
    
    def search_by_description(self, search_term:str)-> List[Expense]:
        """Busca gastos por descripcion"""
        models = self.db.query(ExpenseModel).filter(
            ExpenseModel.description.ilike(f'%{search_term}%')
        ).order_by(ExpenseModel.date.desc()).all()

        return [self._model_to_entity(model) for model in models]
    
    def get_recent_expenses(self, days: int = 30) -> List[Expense]:
        """Obtiene los gastos mas recientes"""
        from datetime import timedelta
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        #model.update_at = datetime.now(timezone.utc) / Linea de referencia
        
        return self.get_by_date_range(cutoff_date,datetime.now(timezone.utc))
    
    def get_monthly_summary(self) -> List[Dict]:
        """
        NUEVO: Obtiene un resumen mensual ( Util para PowerBI)
        Returns: Lista de diccionarios con año, mes, total, count
        """
        results = self.db.query(
            extract('year', ExpenseModel.date).label('year'),
            extract('month', ExpenseModel.date).label('month'),
            func.sum(ExpenseModel.amount).label('total'),
            func.count(ExpenseModel.id).label('count')
        ).group_by('year','month').order_by('year','month').all()

        return[
            {
                'year': int(year),
                'month': int(month),
                'total': float(total),
                'count': count           
            }
            for year, month, total, count in results
        ]

    

    