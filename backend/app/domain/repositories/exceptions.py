class RepositoryError(Exception):
    """ Excepcion base para errores repositorio"""
    pass

class ExpenseNotFoundError(RepositoryError):
    """
    Se lanza cuando no se encuentra un gasto
    """
    def __init__(self, expense_id: int):
        super().__init__(f"Gasto con ID {expense_id} no encontrado")
        self.expense_id = expense_id

"""Se lanza cuando se intenta crear un gasto duplicado"""
class DuplicateExpenseError(RepositoryError):
    def __init__(self, message: str  = "Gasto Duplicado"):
        super().__init__(message)

class RepositoryConnectionError(RepositoryError):
    def __init__(self, message: str = "Error de conexion con el repositorio"):
        super().__init__(message)