import re

def is_email_valid(email) -> bool:
    pattern = (
        r"^(?!\.)"                                # No leading dot
        r"(?!.*\.\.)"                             # No consecutive dots
        r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"       # Local part
        r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"          # Domain part
    )

    return re.fullmatch(pattern, email) is not None
