# tests/test_application/test_use_cases.py
import pytest
from datetime import datetime, timedelta

from app.domain.entities.expense import Expense, PaymentMethod
from app.application.dtos.expense_dto import (
    CreateExpenseDTO, 
    UpdateExpenseDTO,
    ExpenseFilterDTO
)
from app.application.use_cases.create_expense import CreateExpenseUseCase
from app.application.use_cases.get_expense_by_id import GetExpenseByIdUseCase
from app.application.use_cases.get_all_expenses import GetAllExpensesUseCase
from app.application.use_cases.get_filtered_expenses import GetFilteredExpensesUseCase
from app.application.use_cases.update_expense import UpdateExpenseUseCase
from app.application.use_cases.delete_expense import DeleteExpenseUseCase
from app.application.use_cases.get_dashboard_data import GetDashboardDataUseCase
from app.infrastructure.repositories.json_expense_repository import JsonExpenseRepository
from app.domain.repositories.exceptions import ExpenseNotFoundError


class TestCreateExpenseUseCase:
    """Tests para CreateExpenseUseCase"""
    
    @pytest.fixture
    def repository(self, tmp_path):
        """Fixture con repositorio temporal"""
        test_file = tmp_path / "test_expenses.json"
        return JsonExpenseRepository(str(test_file))
    
    @pytest.fixture
    def use_case(self, repository):
        """Fixture con el use case"""
        return CreateExpenseUseCase(repository)
    
    def test_create_expense_successfully(self, use_case, repository):
        """Test: Crear gasto exitosamente"""
        # Arrange
        dto = CreateExpenseDTO(
            amount=25.50,
            category="Comida",
            payment_method="cash",
            description="Almuerzo"
        )
        
        # Act
        result = use_case.execute(dto)
        
        # Assert
        assert result.id is not None
        assert result.amount == 25.50
        assert result.category == "Comida"
        assert result.payment_method == PaymentMethod.CASH
        
        # Verificar que se guardó
        saved = repository.get_by_id(result.id)
        assert saved is not None
    
    def test_create_expense_with_invalid_amount(self, use_case):
        """Test: Crear gasto con monto inválido lanza error"""
        # Arrange
        dto = CreateExpenseDTO(
            amount=-10,  # Monto negativo
            category="Comida",
            payment_method="cash"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="mayor a 0"):
            use_case.execute(dto)
    
    def test_create_expense_with_empty_category(self, use_case):
        """Test: Crear gasto sin categoría lanza error"""
        # Arrange
        dto = CreateExpenseDTO(
            amount=10,
            category="",  # Categoría vacía
            payment_method="cash"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="categoría es requerida"):
            use_case.execute(dto)


class TestGetExpenseByIdUseCase:
    """Tests para GetExpenseByIdUseCase"""
    
    @pytest.fixture
    def repository(self, tmp_path):
        test_file = tmp_path / "test_expenses.json"
        return JsonExpenseRepository(str(test_file))
    
    @pytest.fixture
    def use_case(self, repository):
        return GetExpenseByIdUseCase(repository)
    
    def test_get_existing_expense(self, use_case, repository):
        """Test: Obtener gasto existente"""
        # Arrange
        expense = Expense(25.50, "Comida", PaymentMethod.CASH)
        saved = repository.save(expense)
        
        # Act
        result = use_case.execute(saved.id)
        
        # Assert
        assert result.id == saved.id
        assert result.amount == 25.50
    
    def test_get_non_existing_expense_raises_error(self, use_case):
        """Test: Obtener gasto inexistente lanza error"""
        # Act & Assert
        with pytest.raises(ExpenseNotFoundError):
            use_case.execute(999)


class TestUpdateExpenseUseCase:
    """Tests para UpdateExpenseUseCase"""
    
    @pytest.fixture
    def repository(self, tmp_path):
        test_file = tmp_path / "test_expenses.json"
        return JsonExpenseRepository(str(test_file))
    
    @pytest.fixture
    def use_case(self, repository):
        return UpdateExpenseUseCase(repository)
    
    def test_update_expense_amount(self, use_case, repository):
        """Test: Actualizar monto de un gasto"""
        # Arrange
        expense = Expense(25.50, "Comida", PaymentMethod.CASH)
        saved = repository.save(expense)
        
        dto = UpdateExpenseDTO(
            expense_id=saved.id,
            amount=50.00
        )
        
        # Act
        result = use_case.execute(dto)
        
        # Assert
        assert result.amount == 50.00
        assert result.category == "Comida"  # No cambió
    
    def test_update_multiple_fields(self, use_case, repository):
        """Test: Actualizar múltiples campos"""
        # Arrange
        expense = Expense(25.50, "Comida", PaymentMethod.CASH)
        saved = repository.save(expense)
        
        dto = UpdateExpenseDTO(
            expense_id=saved.id,
            amount=50.00,
            category="Cena",
            payment_method="debit_card"
        )
        
        # Act
        result = use_case.execute(dto)
        
        # Assert
        assert result.amount == 50.00
        assert result.category == "Cena"
        assert result.payment_method == PaymentMethod.DEBIT_CARD
    
    def test_update_non_existing_expense(self, use_case):
        """Test: Actualizar gasto inexistente lanza error"""
        # Arrange
        dto = UpdateExpenseDTO(expense_id=999, amount=50.00)
        
        # Act & Assert
        with pytest.raises(ExpenseNotFoundError):
            use_case.execute(dto)


class TestDeleteExpenseUseCase:
    """Tests para DeleteExpenseUseCase"""
    
    @pytest.fixture
    def repository(self, tmp_path):
        test_file = tmp_path / "test_expenses.json"
        return JsonExpenseRepository(str(test_file))
    
    @pytest.fixture
    def use_case(self, repository):
        return DeleteExpenseUseCase(repository)
    
    def test_delete_existing_expense(self, use_case, repository):
        """Test: Eliminar gasto existente"""
        # Arrange
        expense = Expense(25.50, "Comida", PaymentMethod.CASH)
        saved = repository.save(expense)
        
        # Act
        result = use_case.execute(saved.id)
        
        # Assert
        assert result is True
        assert repository.get_by_id(saved.id) is None
    
    def test_delete_non_existing_expense(self, use_case):
        """Test: Eliminar gasto inexistente retorna False"""
        # Act
        result = use_case.execute(999)
        
        # Assert
        assert result is False


class TestGetFilteredExpensesUseCase:
    """Tests para GetFilteredExpensesUseCase"""
    
    @pytest.fixture
    def repository(self, tmp_path):
        test_file = tmp_path / "test_expenses.json"
        repo = JsonExpenseRepository(str(test_file))
        
        # Agregar gastos de prueba
        repo.save(Expense(10, "Comida", PaymentMethod.CASH))
        repo.save(Expense(20, "Comida", PaymentMethod.DEBIT_CARD))
        repo.save(Expense(30, "Transporte", PaymentMethod.CASH))
        repo.save(Expense(150, "Entretenimiento", PaymentMethod.CREDIT_CARD))
        
        return repo
    
    @pytest.fixture
    def use_case(self, repository):
        return GetFilteredExpensesUseCase(repository)
    
    def test_filter_by_category(self, use_case):
        """Test: Filtrar por categoría"""
        # Arrange
        filters = ExpenseFilterDTO(category="Comida")
        
        # Act
        result = use_case.execute(filters)
        
        # Assert
        assert len(result) == 2
        assert all(e.category == "Comida" for e in result)
    
    def test_filter_by_payment_method(self, use_case):
        """Test: Filtrar por método de pago"""
        # Arrange
        filters = ExpenseFilterDTO(payment_method="cash")
        
        # Act
        result = use_case.execute(filters)
        
        # Assert
        assert len(result) == 2
        assert all(e.payment_method == PaymentMethod.CASH for e in result)
    
    def test_filter_by_amount_range(self, use_case):
        """Test: Filtrar por rango de monto"""
        # Arrange
        filters = ExpenseFilterDTO(min_amount=20, max_amount=100)
        
        # Act
        result = use_case.execute(filters)
        
        # Assert
        assert len(result) == 2
        assert all(20 <= e.amount <= 100 for e in result)
    
    def test_combined_filters(self, use_case):
        """Test: Múltiples filtros combinados"""
        # Arrange
        filters = ExpenseFilterDTO(
            category="Comida",
            payment_method="cash"
        )
        
        # Act
        result = use_case.execute(filters)
        
        # Assert
        assert len(result) == 1
        assert result[0].category == "Comida"
        assert result[0].payment_method == PaymentMethod.CASH


class TestGetDashboardDataUseCase:
    """Tests para GetDashboardDataUseCase"""
    
    @pytest.fixture
    def repository(self, tmp_path):
        test_file = tmp_path / "test_expenses.json"
        repo = JsonExpenseRepository(str(test_file))
        
        # Agregar gastos variados
        today = datetime.now()
        repo.save(Expense(25, "Comida", PaymentMethod.CASH, date=today))
        repo.save(Expense(30, "Comida", PaymentMethod.DEBIT_CARD, date=today))
        repo.save(Expense(50, "Transporte", PaymentMethod.CASH, date=today))
        
        return repo
    
    @pytest.fixture
    def use_case(self, repository):
        return GetDashboardDataUseCase(repository)
    
    def test_dashboard_data_structure(self, use_case):
        """Test: Estructura de datos del dashboard"""
        # Act
        result = use_case.execute(days=30)
        
        # Assert
        assert "period_info" in result
        assert "summary" in result
        assert "by_category" in result
        assert "by_payment_method" in result
        assert "trend" in result
        assert "recent_expenses" in result
    
    def test_dashboard_summary_calculations(self, use_case):
        """Test: Cálculos del resumen"""
        # Act
        result = use_case.execute(days=30)
        
        # Assert
        summary = result["summary"]
        assert summary["total_amount"] == 105.0  # 25 + 30 + 50
        assert summary["expense_count"] == 3
        assert summary["average_per_expense"] == 35.0
    
    def test_dashboard_category_breakdown(self, use_case):
        """Test: Desglose por categorías"""
        # Act
        result = use_case.execute(days=30)
        
        # Assert
        by_category = result["by_category"]
        assert by_category["totals"]["Comida"] == 55.0  # 25 + 30
        assert by_category["totals"]["Transporte"] == 50.0
        assert by_category["counts"]["Comida"] == 2


# =============================================================================
# TEST MANUAL SIMPLE
# =============================================================================

if __name__ == "__main__":
    """
    Test simple que puedes ejecutar con: python test_use_cases.py
    """
    print("🧪 Ejecutando tests manuales de Use Cases...\n")
    
    # Setup
    repo = JsonExpenseRepository("test_use_cases_manual.json")
    repo.clear_all()
    
    # Test 1: Crear gasto
    print("✓ Test 1: CreateExpenseUseCase")
    create_use_case = CreateExpenseUseCase(repo)
    dto = CreateExpenseDTO(
        amount=25.50,
        category="Comida",
        payment_method="cash",
        description="Almuerzo"
    )
    expense = create_use_case.execute(dto)
    print(f"  Gasto creado: {expense}")
    
    # Test 2: Obtener por ID
    print("\n✓ Test 2: GetExpenseByIdUseCase")
    get_use_case = GetExpenseByIdUseCase(repo)
    retrieved = get_use_case.execute(expense.id)
    print(f"  Gasto recuperado: {retrieved}")
    
    # Test 3: Actualizar
    print("\n✓ Test 3: UpdateExpenseUseCase")
    update_use_case = UpdateExpenseUseCase(repo)
    update_dto = UpdateExpenseDTO(expense_id=expense.id, amount=50.00)
    updated = update_use_case.execute(update_dto)
    print(f"  Monto actualizado: ${updated.amount}")
    
    # Test 4: Dashboard
    print("\n✓ Test 4: GetDashboardDataUseCase")
    # Crear más gastos
    create_use_case.execute(CreateExpenseDTO(15, "Transporte", "debit_card"))