from datetime import datetime
from typing import Optional
from enum import Enum

class PaymentMethod(Enum):
    #Formas de pago disponibles
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    #TRANSFER = "transfer" #yo cree esta forma de pago

class Expense:
    """
Entidad Expense - Nucleo del dominio
Esta clase contiene SOLO la logica del nogocio pura
No sabe nada sobre base de datos , API's o framework
"""

    def __init__(
        self,
        amount: float,
        category: str,
        payment_method: PaymentMethod,
        date: Optional[datetime] = None,
        description: Optional[str] = None,
        id: Optional[int] = None
    ):

# Validaciones de negocio - Reglas de la aplicacion
        if amount <= 0:
            raise ValueError("El monto del gasto debe ser mayor que cero.")
        if not category or category.strip() == "":
            raise ValueError ("La catergoria es requerida")

        if not isinstance(payment_method,PaymentMethod):
            raise ValueError("Metodo de Pago invalido")

#Asignacion de Valores

        self.id = id
        self.amount = round(amount,2)  # Redondear a 2 decimales
        self.category = category.strip().title()  # Formatear categoria
        self.payment_method = payment_method        
        self.date = date or datetime.now()  # Alternativa usando 'or' CLAUDE
        self.description = description.strip() if description else None  # Limpiar descripcion


    def update_amount(self, new_amount: float) -> None:
        """Actualiza el monto del gasto, asegurando que sea mayor que cero y redondeado a dos decimales.
       Es una definicion del negocio para actualizar el monto del gasto. 
    """
        if new_amount <= 0:
            raise ValueError("El monto del gasto debe ser mayor que cero.")
        self.amount = round(new_amount, 2)

    def update_category(self, new_category: str)-> None:
        """ Actualiza la categoria de gasto, asegurando que no este vacia y formateada correctamente.
        Regla del negocio: no puede estar vacia
        Esta parte no entiendo muy bien actualizar, no seria crear?
        """
        if not  new_category or new_category.strip() == "":
            raise ValueError("La categoria es requerida.")
        self.category = new_category.strip().title()    

    
    def is_recent(self, days: int=30  ) -> bool:
        """Determina si el gasto es reciente, dentro de los ultimos 'days' dias.
       Regla del negocio: definir que es un gasto reciente
       No se si esto, realmente sea aplicable
    """
        from datetime import datetime, timedelta
        return (datetime.now() - self.date).days <=  days

    def is_high_amount(self, threshold: float = 100.0)-> bool:
        """
    Determina si un gasto es alto 
    Regla del negocio: alto, mayor al umbral 
    """
        return self.amount > threshold

    def get_formatted_amount(self) -> str:
    #def get_formatted_amount(self) -> str:
        """
        Retorna el monto formateado para mostrar
        """
        return f"${self.amount:,.2f}"
        #return f"${self.amount:,.2f}"
        
    def to_dict(self) -> dict:
        """
        Convierte la entidad a diccionario
        Útil para serialización
        """
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "payment_method": self.payment_method.value,
            "date": self.date.isoformat() if self.date else None,
            "description": self.description
        }   

    def __str__(self) -> str:
        """Representación en string del gasto"""
        return f"Gasto: {self.get_formatted_amount()} - {self.category} ({self.payment_method.value})"
        #return f"Gasto: {self.get_formatted_amount()} - {self.category} ({self.payment_method.value})"

    def __repr__(self) -> str:
        """Representación técnica del gasto"""
        return f"Expense(id={self.id}, amount={self.amount}, category='{self.category}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos gastos"""
        if not isinstance(other, Expense):
            return False
        return (
            self.amount == other.amount and
            self.category == other.category and
            self.payment_method == other.payment_method and
            self.date == other.date
        )

