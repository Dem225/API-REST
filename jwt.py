import os

from dotenv import load_dotenv
from jose import jwt, JWTError
from loguru import logger

from datetime import datetime, timezone, timedelta


TIME_ACCESS = 5

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if SECRET_KEY:
    SECRET_KEY = SECRET_KEY.strip().strip('"').strip("'")
if not SECRET_KEY:
    # Ne pas planter à l'import : l'API doit pouvoir répondre au health check.
    # L'erreur est levée explicitement lors de la création/vérification d'un token.
    logger.warning(
        "JWT_SECRET_KEY n'est pas défini : les routes d'authentification sont désactivées."
    )
ALGORITHM = "HS256"


def _get_secret_key() -> str:
    if not SECRET_KEY:
        raise RuntimeError(
            "JWT_SECRET_KEY n'est pas défini : ajoute-le dans ton fichier .env "
            "(voir .env.example) ou dans le dashboard FastAPI Cloud."
        )
    return SECRET_KEY


def create_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TIME_ACCESS
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        _get_secret_key(),
        algorithm=ALGORITHM
    )


def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            _get_secret_key(),
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError as e:

        print("ERREUR JWT :", e)

        return None