from fastapi_users import FastAPIUsers
from backend.database.models import User
from backend.database.schemas import UserCreate, UserRead, UserUpdate
from backend.database.user_db import get_user_db
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy

SECRET = "YOUR_SECRET_KEY"

cookie_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

current_user = fastapi_users.current_user()

router = fastapi_users.get_auth_router(auth_backend)
