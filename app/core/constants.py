from enum import Enum


class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    READER = "reader"


class BookStatus(str, Enum):
    """Book status."""
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    LOST = "lost"
    DAMAGED = "damaged"


class LoanStatus(str, Enum):
    """Loan status."""
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    LOST = "lost"
    DAMAGED = "damaged"


class ReservationStatus(str, Enum):
    """Reservation status."""
    PENDING = "pending"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# Cache keys
CACHE_KEYS = {
    "BOOKS": "books",
    "USERS": "users",
    "LOANS": "loans",
    "RESERVATIONS": "reservations"
}

# Error messages
ERROR_MESSAGES = {
    "NOT_FOUND": "Resource not found",
    "VALIDATION_ERROR": "Validation error",
    "AUTHENTICATION_ERROR": "Authentication failed",
    "AUTHORIZATION_ERROR": "Not enough permissions",
    "CONFLICT_ERROR": "Resource conflict",
    "BUSINESS_RULE_ERROR": "Business rule violation"
}

# Success messages
SUCCESS_MESSAGES = {
    "CREATED": "Resource created successfully",
    "UPDATED": "Resource updated successfully",
    "DELETED": "Resource deleted successfully",
    "RETRIEVED": "Resource retrieved successfully"
}

# Business rules
BUSINESS_RULES = {
    "MAX_LOANS_PER_USER": 3,
    "MAX_RESERVATIONS_PER_USER": 2,
    "LOAN_DURATION_DAYS": 15,
    "RESERVATION_DURATION_DAYS": 7,
    "OVERDUE_FINE_PER_DAY": 1.0
} 