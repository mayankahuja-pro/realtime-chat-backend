from app.core.security import (
    hash_password,
    verify_password,
)

password = "Mayank@123"

hashed = hash_password(password)

print("Hash:", hashed)

print(
    verify_password(password, hashed)
)