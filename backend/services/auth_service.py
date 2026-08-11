from typing import Optional
from backend.database.session import get_db_session
from backend.repositories.user_repository import UserRepository
from backend.auth.password import hash_password, verify_password
from backend.schemas.user import UserCreate, UserResponse
from backend.utils.exceptions import AuthenticationError, ValidationError
from backend.validators.input_validators import validate_email

class AuthService:
    """Enterprise authentication service managing user registration and credential verification."""

    def register_user(self, user_in: UserCreate) -> UserResponse:
        """Register a new enterprise user.

        Args:
            user_in (UserCreate): Validated user creation payload.

        Returns:
            UserResponse: Serialized user response object.

        Raises:
            ValidationError: If email format is invalid or username/email is already taken.
        """
        validate_email(user_in.email)
        with get_db_session() as session:
            repo = UserRepository(session)
            if repo.get_by_username(user_in.username):
                raise ValidationError(f"Username '{user_in.username}' is already taken.")
            if repo.get_by_email(user_in.email):
                raise ValidationError(f"Email '{user_in.email}' is already registered.")

            user_data = user_in.model_dump()
            raw_password = user_data.pop("password")
            user_data["password_hash"] = hash_password(raw_password)

            created_user = repo.create(user_data)
            return UserResponse.model_validate(created_user)

    def authenticate_user(self, username: str, password: str) -> UserResponse:
        """Authenticate user credentials and update last login timestamp.

        Args:
            username (str): Target username or email address.
            password (str): Raw password string.

        Returns:
            UserResponse: Authenticated user metadata.

        Raises:
            AuthenticationError: If credentials fail verification or account is inactive.
        """
        with get_db_session() as session:
            repo = UserRepository(session)
            user = repo.get_by_username(username) or repo.get_by_email(username)
            if not user or not verify_password(password, user.password_hash):
                raise AuthenticationError("Invalid username or password.")
            if not user.is_active or user.is_deleted:
                raise AuthenticationError("Account is inactive or suspended.")

            repo.update_last_login(user.id)
            return UserResponse.model_validate(user)


auth_service = AuthService()
