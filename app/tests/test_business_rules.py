import pytest
from datetime import datetime, timedelta
from app.core.exceptions import BusinessRuleException
from app.core.constants import BUSINESS_RULES
from app.business.biblioteca_rules import BibliotecaRules


def test_max_loans_per_user(db, test_user, test_book):
    """Test maximum loans per user rule."""
    rules = BibliotecaRules(db)
    
    # Create maximum allowed loans
    for i in range(BUSINESS_RULES["MAX_LOANS_PER_USER"]):
        rules.create_loan(test_user.id, test_book.id)
    
    # Try to create one more loan
    with pytest.raises(BusinessRuleException) as exc_info:
        rules.create_loan(test_user.id, test_book.id)
    
    assert "Maximum loans exceeded" in str(exc_info.value)


def test_max_reservations_per_user(db, test_user, test_book):
    """Test maximum reservations per user rule."""
    rules = BibliotecaRules(db)
    
    # Create maximum allowed reservations
    for i in range(BUSINESS_RULES["MAX_RESERVATIONS_PER_USER"]):
        rules.create_reservation(test_user.id, test_book.id)
    
    # Try to create one more reservation
    with pytest.raises(BusinessRuleException) as exc_info:
        rules.create_reservation(test_user.id, test_book.id)
    
    assert "Maximum reservations exceeded" in str(exc_info.value)


def test_loan_duration(db, test_user, test_book):
    """Test loan duration rule."""
    rules = BibliotecaRules(db)
    
    # Create loan
    loan = rules.create_loan(test_user.id, test_book.id)
    
    # Check due date
    expected_due_date = datetime.now() + timedelta(
        days=BUSINESS_RULES["LOAN_DURATION_DAYS"]
    )
    assert abs((loan.data_devolucao - expected_due_date).total_seconds()) < 1


def test_reservation_duration(db, test_user, test_book):
    """Test reservation duration rule."""
    rules = BibliotecaRules(db)
    
    # Create reservation
    reservation = rules.create_reservation(test_user.id, test_book.id)
    
    # Check expiration date
    expected_expiration = datetime.now() + timedelta(
        days=BUSINESS_RULES["RESERVATION_DURATION_DAYS"]
    )
    assert abs(
        (reservation.data_expiracao - expected_expiration).total_seconds()
    ) < 1


def test_overdue_fine(db, test_user, test_book):
    """Test overdue fine calculation."""
    rules = BibliotecaRules(db)
    
    # Create loan
    loan = rules.create_loan(test_user.id, test_book.id)
    
    # Set return date to 5 days after due date
    return_date = loan.data_devolucao + timedelta(days=5)
    
    # Calculate fine
    fine = rules.calculate_fine(loan.data_devolucao, return_date)
    
    # Check fine amount
    expected_fine = 5 * BUSINESS_RULES["OVERDUE_FINE_PER_DAY"]
    assert fine == expected_fine 