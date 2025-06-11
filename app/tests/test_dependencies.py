import pytest
from app.core.dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_admin_user
)
from app.core.exceptions import (
    AuthenticationException,
    AuthorizationException
)


def test_get_current_user(db, test_user):
    """Test get current user dependency."""
    # Test with valid token
    user = get_current_user(db, test_user.id)
    assert user.id == test_user.id
    assert user.email == test_user.email
    
    # Test with invalid token
    with pytest.raises(AuthenticationException):
        get_current_user(db, "invalid_token")
    
    # Test with non-existent user
    with pytest.raises(AuthenticationException):
        get_current_user(db, 999)


def test_get_current_active_user(db, test_user):
    """Test get current active user dependency."""
    # Test with active user
    user = get_current_active_user(test_user)
    assert user.id == test_user.id
    assert user.is_active
    
    # Test with inactive user
    test_user.is_active = False
    with pytest.raises(AuthorizationException):
        get_current_active_user(test_user)


def test_get_current_admin_user(db, test_user):
    """Test get current admin user dependency."""
    # Test with admin user
    test_user.role = "admin"
    user = get_current_admin_user(test_user)
    assert user.id == test_user.id
    assert user.role == "admin"
    
    # Test with non-admin user
    test_user.role = "user"
    with pytest.raises(AuthorizationException):
        get_current_admin_user(test_user)


def test_dependency_injection(db, test_user):
    """Test dependency injection chain."""
    # Test full chain
    user = get_current_user(db, test_user.id)
    active_user = get_current_active_user(user)
    admin_user = get_current_admin_user(active_user)
    
    assert admin_user.id == test_user.id
    assert admin_user.is_active
    assert admin_user.ativo is True
    assert admin_user.admin is True


def test_dependency_error_handling(db):
    """Test dependency error handling."""
    # Test missing token
    with pytest.raises(AuthenticationException):
        get_current_user(db, None)
    
    # Test invalid token format
    with pytest.raises(AuthenticationException):
        get_current_user(db, "invalid.token.format")
    
    # Test token with invalid payload
    from app.core.security import create_access_token
    token = create_access_token({"invalid": "payload"})
    with pytest.raises(AuthenticationException):
        get_current_user(db, token) 