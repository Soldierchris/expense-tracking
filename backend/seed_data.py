# backend/seed_data.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.models import ExpenseModel, PaymentMethodEnum
from datetime import datetime

def seed_data():
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        count = db.query(ExpenseModel).count()
        if count > 0:
            print(f"✅ Ya hay {count} gastos en la base de datos")
            return
        
        # Crear gastos de prueba
        expenses = [
            ExpenseModel(
                amount=25.50,
                category="Comida",
                payment_method=PaymentMethodEnum.CASH,
                description="Almuerzo restaurante",
                date=datetime.now()
            ),
            ExpenseModel(
                amount=15.00,
                category="Transporte",
                payment_method=PaymentMethodEnum.DEBIT_CARD,
                description="Uber",
                date=datetime.now()
            ),
            ExpenseModel(
                amount=50.00,
                category="Entretenimiento",
                payment_method=PaymentMethodEnum.CREDIT_CARD,
                description="Cine",
                date=datetime.now()
            ),
        ]
        
        for expense in expenses:
            db.add(expense)
        
        db.commit()
        print(f"✅ Se agregaron {len(expenses)} gastos de prueba")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()