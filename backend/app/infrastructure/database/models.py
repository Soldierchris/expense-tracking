# app/infrastructure/database/models.py
from sqlalchemy import Column, Integer, Float, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from datetime import timezone
import enum

Base=declarative_base()

class PaymentMethodEnum(str, enum.Enum):
    """
    Enum para metodos de pago en la base de datos
    """
    CASH= "cash"
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"

class ExpenseModel(Base):
    """
    Modelo SQLAlchemy para la tabla de gastos
    Representa la estructura de la tabla en PostgreSQL
    """
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float, nullable=False, index=True)
    category =Column(String(100), nullable=False, index=True)
    payment_method = Column(Enum(PaymentMethodEnum), nullable=False, index=True)
    #date = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    description = Column(String(500), nullable=True)
    #created_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    #update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    update_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, category={self.category})>"
    
    