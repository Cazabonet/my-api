from app.core.constants import (
    UserRole,
    BookStatus,
    LoanStatus,
    ReservationStatus,
    CACHE_KEYS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    BUSINESS_RULES
)


def test_user_roles():
    """Test user roles enum."""
    assert UserRole.ADMIN == "admin"
    assert UserRole.LIBRARIAN == "librarian"
    assert UserRole.READER == "reader"
    
    # Test enum values
    assert list(UserRole) == ["admin", "librarian", "reader"]
    
    # Test enum membership
    assert "admin" in UserRole
    assert "invalid" not in UserRole


def test_book_status():
    """Test book status enum."""
    assert BookStatus.AVAILABLE == "available"
    assert BookStatus.BORROWED == "borrowed"
    assert BookStatus.RESERVED == "reserved"
    assert BookStatus.LOST == "lost"
    assert BookStatus.DAMAGED == "damaged"
    
    # Test enum values
    assert list(BookStatus) == [
        "available",
        "borrowed",
        "reserved",
        "lost",
        "damaged"
    ]
    
    # Test enum membership
    assert "available" in BookStatus
    assert "invalid" not in BookStatus


def test_loan_status():
    """Test loan status enum."""
    assert LoanStatus.ACTIVE == "active"
    assert LoanStatus.RETURNED == "returned"
    assert LoanStatus.OVERDUE == "overdue"
    assert LoanStatus.LOST == "lost"
    assert LoanStatus.DAMAGED == "damaged"
    
    # Test enum values
    assert list(LoanStatus) == [
        "active",
        "returned",
        "overdue",
        "lost",
        "damaged"
    ]
    
    # Test enum membership
    assert "active" in LoanStatus
    assert "invalid" not in LoanStatus


def test_reservation_status():
    """Test reservation status enum."""
    assert ReservationStatus.PENDING == "pending"
    assert ReservationStatus.FULFILLED == "fulfilled"
    assert ReservationStatus.CANCELLED == "cancelled"
    assert ReservationStatus.EXPIRED == "expired"
    
    # Test enum values
    assert list(ReservationStatus) == [
        "pending",
        "fulfilled",
        "cancelled",
        "expired"
    ]
    
    # Test enum membership
    assert "pending" in ReservationStatus
    assert "invalid" not in ReservationStatus


def test_cache_keys():
    """Test cache keys."""
    assert CACHE_KEYS["BOOKS"] == "books"
    assert CACHE_KEYS["USERS"] == "users"
    assert CACHE_KEYS["LOANS"] == "loans"
    assert CACHE_KEYS["RESERVATIONS"] == "reservations"
    
    # Test dictionary keys
    assert set(CACHE_KEYS.keys()) == {
        "BOOKS",
        "USERS",
        "LOANS",
        "RESERVATIONS"
    }


def test_error_messages():
    """Test error messages."""
    assert ERROR_MESSAGES["NOT_FOUND"] == "Resource not found"
    assert ERROR_MESSAGES["VALIDATION_ERROR"] == "Validation error"
    assert ERROR_MESSAGES["AUTHENTICATION_ERROR"] == "Authentication failed"
    assert ERROR_MESSAGES["AUTHORIZATION_ERROR"] == "Not enough permissions"
    assert ERROR_MESSAGES["CONFLICT_ERROR"] == "Resource conflict"
    assert ERROR_MESSAGES["BUSINESS_RULE_ERROR"] == "Business rule violation"
    
    # Test dictionary keys
    assert set(ERROR_MESSAGES.keys()) == {
        "NOT_FOUND",
        "VALIDATION_ERROR",
        "AUTHENTICATION_ERROR",
        "AUTHORIZATION_ERROR",
        "CONFLICT_ERROR",
        "BUSINESS_RULE_ERROR"
    }


def test_success_messages():
    """Test success messages."""
    assert SUCCESS_MESSAGES["CREATED"] == "Resource created successfully"
    assert SUCCESS_MESSAGES["UPDATED"] == "Resource updated successfully"
    assert SUCCESS_MESSAGES["DELETED"] == "Resource deleted successfully"
    assert SUCCESS_MESSAGES["RETRIEVED"] == "Resource retrieved successfully"
    
    # Test dictionary keys
    assert set(SUCCESS_MESSAGES.keys()) == {
        "CREATED",
        "UPDATED",
        "DELETED",
        "RETRIEVED"
    }


def test_business_rules():
    """Test business rules."""
    assert BUSINESS_RULES["MAX_LOANS_PER_USER"] == 3
    assert BUSINESS_RULES["MAX_RESERVATIONS_PER_USER"] == 2
    assert BUSINESS_RULES["LOAN_DURATION_DAYS"] == 15
    assert BUSINESS_RULES["RESERVATION_DURATION_DAYS"] == 7
    assert BUSINESS_RULES["OVERDUE_FINE_PER_DAY"] == 1.0
    
    # Test dictionary keys
    assert set(BUSINESS_RULES.keys()) == {
        "MAX_LOANS_PER_USER",
        "MAX_RESERVATIONS_PER_USER",
        "LOAN_DURATION_DAYS",
        "RESERVATION_DURATION_DAYS",
        "OVERDUE_FINE_PER_DAY"
    } 