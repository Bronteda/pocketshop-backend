from dataclasses import dataclass
from django.utils.crypto import get_random_string

@dataclass
class AuthResult:
    ok: bool
    auth_id: str | None = None


class MockPaymentService:
    def authorize(self, *, exp_month: int, exp_year: int) -> AuthResult:
        # Serializer already guarantees card is not expired
        return AuthResult(ok=True, auth_id=f"mock_auth_{get_random_string(8)}")