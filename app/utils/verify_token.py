from jose import jwt, JWTError

PUBLIC_KEY = open("keys/oauth-public.key").read()

ALGORITHM = "RS256"


def verify_token(token: str):
    try:
        # token = token.replace("Bearer ", "", 1).strip()
        print(token,'is the key')
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])

        return payload  # contains user info

    except JWTError:
        return None
