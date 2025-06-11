from sqlalchemy import Column, Boolean
from datetime import datetime


class TimestampMixin:
    """Mixin for timestamp fields."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        """Mark record as deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restore deleted record."""
        self.is_deleted = False
        self.deleted_at = None


class ValidationMixin:
    """Mixin for common validations."""
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Validate Brazilian CPF."""
        if not cpf or len(cpf) != 11:
            return False
        return cpf.isdigit()

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        if not email or '@' not in email:
            return False
        return True

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number."""
        if not phone or len(phone) != 11:
            return False
        return phone.isdigit() 