from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
from ..entities.expense import Expense

class ExpenseRepository(ABC):
    """
    Interface que defini QUÉ operaciones necesitamos con gastos

    Esta es una INTERFACE (contrato) - define QUÉ hacer, NO COMO HACERLO
    Las implementaciones concretas (JSON, MYSQL, PostgreeSQL, etc), definirán el cómo

    Por qué usamos interfaces? 
    - Podemos cambiar de JSON a PostgreeSQL sin romper nada
    - Podemos probar con datos fake facilmente
    - La lógica del negocio no depende de detalles técnicos
    """
    @abstractmethod
    def save(self,expense: Expense) -> Expense:
        """
        Guarda un gasto nuevo 

        Args: 
            expense: El gasto a guardar

        Returns:
            Expense: El gasto guardado con ID asignado

        Raises:
            RepositoryError: Si no se puede guardar
        """
        pass

    @abstractmethod
    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        """
        Obtiene un gasto por su ID
        Args: expense_ide: ID del gasto a buscar
        Returns: Optional[Expense]: El gasto si existe, None si no existe
        """
        pass
    @abstractmethod
    def get_all(self) -> List[Expense]:
        """
        Obtiene todos los gastos
        Returns: List[Expense]: Lista de todos los gastos
        """
        pass

    @abstractmethod
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    )-> List[Expense]:
        """
        Obtiene gastos en un rango de fechas
        Args: start_date: Fecha inicial (inclusive)
              end_date: Fecha Final (inclusive )
        Returns: List[Expense]: Lista de gastos en el rango
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Expense]:
        """
        Obtiene gastos de una categoria especifica
        Args: category: Nombre de la categoria
        Returnd: List[Expense]: Lista de Gastos de esa categoria
        """
        pass
    @abstractmethod
    def get_by_payment_method(self,payment_method:str)-> List[Expense]:
        """
        Obtiene gastos por método de pago
        Args: payment_method: Metodo de pago(cash, debit_card,credit_card)    
        Returns: List[Expense]: Lista de pago con ese método de pago
        """
        pass

    @abstractmethod
    def update(self, expense: Expense) -> Expense:
        """
        Actauliza el gasto existente
        Args: expense: El gasto con los datos actualizados
        Returns: Expense: El gastro Actualizado
        Raises: RepositoryError: Si no se puede actualizar el repositorio o no existe        """
        pass

    @abstractmethod
    def delete(self, expense_id:int) -> bool:
        """
        Elimina un gasto por ID
        Args: expense_id: ID del gasto a eliminar 
        Returns: bool: True si se eliminóm, False si no existia
        """
        pass
    @abstractmethod
    def get_total_by_category(self) -> Dict[str, float]:
        """
        Obtiene totales agrupados por categoria
        Returns: 
            Dict[str,float]: Diccionario con categoria -> total gastado
            Ejemplo: {"Comida": 150.50, "Transporte": 45.00}
        """
        pass

    @abstractmethod
    def get_total_by_payment_method(self) -> Dict[str,float:]:
        """
        Obtiene totales agrupados por metodo de pago 
        Returns:
            Dict[str,float]: DIccionario con metodo->total gastado
            Ejemplo_. {"cash": 95.50, "debit_card": 200.00}
        """
        pass

    @abstractmethod
    def get_count_by_category(self) -> Dict[str,int]:
        """
        Obtiene cantidad de gastos por categoria
        Returns: 
            Dicts[str.int]: Diccionario con categoria -> cantidad
            Ejemplo:{"Comida": 76, "Transporte": 3}
        """
        pass

    @abstractmethod
    def search_by_description(self, search_term: str)-> List[Expense]:
        """
        Busca gastos por descripcion (busqueda parcial)
        Args: search:term: Termino a buscar en las descripciones
        Returns: List[Expense]: Lista de gastos que coinciden
        """
        pass

    @abstractmethod
    def get_recent_expenses(self, days: int =30) -> List[Expense]:
        """
        Obtiene los gastos de los ultimonos N dias
        ARgs: Numero de dias hacia atras
        Returns: List[Expense: Lista de gastos recientes]
        """
        pass

