from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

# cookie
cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name='cookie')

# jwt strategy
SECRET = "SECRET"  # this secret variable we need to write in our .env file and then use in config.py in real project


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
