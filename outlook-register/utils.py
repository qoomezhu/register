from __future__ import annotations

import secrets
import string
import random
from typing import Tuple


def generate_strong_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = "".join(secrets.choice(chars) for _ in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%^&*" for c in password)
        ):
            return password


def random_email(length: int) -> str:
    first_char = secrets.choice(string.ascii_lowercase)
    other_chars = []
    for _ in range(length - 1):
        if random.random() < 0.07:
            other_chars.append(secrets.choice(string.digits))
        else:
            other_chars.append(secrets.choice(string.ascii_lowercase))
    return first_char + "".join(other_chars)


def pick_email_and_password() -> Tuple[str, str]:
    email = random_email(random.randint(12, 14))
    password = generate_strong_password(random.randint(11, 15))
    return email, password
