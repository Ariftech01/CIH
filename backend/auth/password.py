import hashlib
import os
import secrets

try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    HAS_PASSLIB = True
except ImportError:
    pwd_context = None
    HAS_PASSLIB = False

def hash_password(password: str) -> str:
    """
    Hashes raw password using passlib (bcrypt) or PBKDF2 HMAC SHA256 fallback.
    """
    if HAS_PASSLIB and pwd_context:
        try:
            return pwd_context.hash(password)
        except Exception:
            pass

    # Standard library fallback using PBKDF2 HMAC SHA256
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"pbkdf2_sha256${salt}${key}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies plain password against hashed password.
    """
    if HAS_PASSLIB and pwd_context and not hashed_password.startswith("pbkdf2_sha256$"):
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            pass

    if hashed_password.startswith("pbkdf2_sha256$"):
        try:
            parts = hashed_password.split("$")
            if len(parts) == 3:
                salt = parts[1]
                stored_key = parts[2]
                key = hashlib.pbkdf2_hmac(
                    'sha256',
                    plain_password.encode('utf-8'),
                    salt.encode('utf-8'),
                    100000
                ).hex()
                return secrets.compare_digest(key, stored_key)
        except Exception:
            return False

    return False
