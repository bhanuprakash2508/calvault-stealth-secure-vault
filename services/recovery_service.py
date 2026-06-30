import secrets
import string


def generate_recovery_key():

    chars = string.ascii_uppercase + string.digits

    parts = [

        ''.join(
            secrets.choice(chars)
            for _ in range(4)
        )

        for _ in range(4)
    ]

    return f"CV-{'-'.join(parts)}"