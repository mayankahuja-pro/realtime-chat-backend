from jose import JWTError

from app.core.auth import decode_token


async def get_user_id_from_token(token: str):
    try:
        payload = decode_token(token)

        print("JWT Payload:", payload)

        return str(payload.get("sub"))

    except JWTError as e:
        print("JWT Error:", e)
        return None