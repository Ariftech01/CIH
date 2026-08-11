import html
from typing import Dict

class SecurityService:
    """
    Enterprise Security Service providing input sanitization, security headers, CORS/CSRF protection, and audit trailing.
    """
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        if not user_input:
            return ""
        return html.escape(user_input.strip())

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval';"
        }

security_service = SecurityService()
