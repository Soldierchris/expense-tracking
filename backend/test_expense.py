
#test_expense.py solo para probar 
#pero que prueba? 
from app.domain.entities.expense import Expense, PaymentMethod
#from app.domain.entities.expenseclaude import Expense, PaymentMethod
#Probar creación de gasto
expense = Expense(
    amount=25.50,
    category="comida",
    payment_method=PaymentMethod.CASH,
    description="ALmuerzo con el Jefe"
)
print(expense)
print(f"Es reciente? {expense.is_recent()}")
print(f"Es alto? {expense.is_high_amount()}")
