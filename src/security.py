import os
import hashlib
import binascii

def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt = binascii.hexlify(os.urandom(16)).decode()
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash

if __name__ == "__main__":
    pw = "mysecret"
    hash_val, salt_val = hash_password(pw)
    print("Hash:", hash_val)
    print("Salt:", salt_val)

    print("Verify correct password:", verify_password("mysecret", hash_val, salt_val))
    print("Verify wrong password:", verify_password("wrongpass", hash_val, salt_val))
