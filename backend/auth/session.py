from typing import Dict, Any, Optional
from backend.auth.password import verify_password
from backend.app_logging.logger import auth_logger

class AuthSessionManager:
    """
    In-memory / backend session validation helper supporting existing Admin login.
    """
    def authenticate_admin(self, username_or_email: str, password_hash: str, input_password: str) -> bool:
        is_valid = verify_password(input_password, password_hash)
        if is_valid:
            auth_logger.info(f"Successful authentication for user: {username_or_email}")
        else:
            auth_logger.warning(f"Failed authentication attempt for user: {username_or_email}")
        return is_valid

auth_session_manager = AuthSessionManager()
