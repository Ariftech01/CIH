import re
from backend.utils.exceptions import ValidationError

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def validate_email(email: str) -> str:
    if not email or not EMAIL_REGEX.match(email):
        raise ValidationError(f"Invalid email address format: '{email}'")
    return email

def validate_positive_number(val: float, field_name: str) -> float:
    if val is None or val < 0:
        raise ValidationError(f"Field '{field_name}' must be a non-negative number. Got: {val}")
    return val

def validate_strictly_positive_number(val: float, field_name: str) -> float:
    if val is None or val <= 0:
        raise ValidationError(f"Field '{field_name}' must be greater than zero. Got: {val}")
    return val

def validate_percentage(val: float, field_name: str = "completion_percentage") -> float:
    if val is None or val < 0 or val > 100:
        raise ValidationError(f"Field '{field_name}' must be between 0 and 100. Got: {val}")
    return val

def validate_project_code(code: str) -> str:
    if not code or len(code.strip()) == 0:
        raise ValidationError("Project code cannot be empty.")
    return code.strip().upper()
