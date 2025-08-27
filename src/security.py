
import os, hashlib, binascii

def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """
    Returns (password_hash, salt). Uses SHA-256 with a random hex salt.
    Not for production, but OK for learning.
    """
    if salt is None:
        salt = binascii.hexlify(os.urandom(16)).decode()
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
