from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_text: str) -> str:
    """
    Cryptographically converts a plain text password into a hash for storage.
    """
    return password_context.hash(plain_text)


def verify_password(plain_text, hashed) -> bool:
    """
    Hashes the provided plain text password and compares it to the stored hash for the user.
    """
    return password_context.verify(plain_text, hashed)
