import os
import jwt
from flask import request


def token_url(id, email, expiry_date):
    email = email.lower()
    secret_key = os.environ.get("JWT_SECRET")
    algorithm = os.environ.get("JWT_ALGORITHM")

    token = jwt.encode(
        {"id": id, "email": email, "exp": expiry_date}, secret_key, algorithm=algorithm
    )
    url = request.base_url
    full_url = url + "create_password?token={}".format(token.decode("ascii"))
    return full_url
