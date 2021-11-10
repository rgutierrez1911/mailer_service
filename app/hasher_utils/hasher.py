import hmac
import hashlib
import uuid
import secrets 
salt = secrets.token_hex(8)


def salted_password(text: str):
    encoded_text = f"{text}{salt}".encode()
    hashed_text = hashlib.sha256(encoded_text).hexdigest()
    salted_text = f"{hashed_text}:{salt}"
    return salted_text


def validate_password(text: str, secret_text: str):
    salt_part: str = secret_text.split(":")[-1]
    based_text: str = f"{text}{salt_part}".encode()
    hashed_text = hashlib.sha256(based_text).hexdigest()
    complete_text = f"{hashed_text}:{salt}"
    validated = hmac.compare_digest(secret_text, complete_text)

    return validated

