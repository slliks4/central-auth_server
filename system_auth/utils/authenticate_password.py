# Typing Annotation Import
from typing import Tuple, Optional

# C -> Character, P -> Password
def is_long_enough(p) -> bool: return len(p) >= 8
def has_uppercase(p) -> bool: return any(c.isupper() for c in p)
def has_lowercase(p) -> bool: return any(c.islower() for c in p)
def has_digit(p) -> bool: return any(c.isdigit() for c in p)

checks = [
    (is_long_enough, "Must be at least 8 Characters"),
    (has_uppercase, "Must contain an uppercase letter"),
    (has_lowercase, "Must contain a lowercase letter"),
    (has_digit, "Must contain a digit"),
]

def is_password_authentic(password, confirm_password) -> Tuple[bool, Optional[str]]:
    if password != confirm_password:
        return False, "Password Missmatch"

    for check_func, error_msg in checks:
        if not check_func(password):
            return False, f"Password {error_msg}"

    return True, None
