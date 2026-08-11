from typing import List
from backend.config.constants import (
    ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_SITE_ENGINEER, 
    ROLE_SAFETY_OFFICER, ROLE_ESTIMATOR, ROLE_VIEWER
)
from backend.utils.exceptions import PermissionDeniedError

ROLE_HIERARCHY = {
    ROLE_ADMIN: 100,
    ROLE_PROJECT_MANAGER: 80,
    ROLE_SITE_ENGINEER: 60,
    ROLE_SAFETY_OFFICER: 60,
    ROLE_ESTIMATOR: 60,
    ROLE_VIEWER: 10,
}

def has_role(user_role: str, required_roles: List[str]) -> bool:
    if user_role == ROLE_ADMIN:
        return True
    return user_role in required_roles

def check_permission(user_role: str, required_roles: List[str]):
    if not has_role(user_role, required_roles):
        raise PermissionDeniedError(f"User role '{user_role}' does not have required permissions: {required_roles}")
    return True
