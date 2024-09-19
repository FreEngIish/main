from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from routers.auth_routes import router as auth_router
from routers.auth_token_routes import router as auth_token_router

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='your-secret-key')
app.include_router(auth_router)
app.include_router(auth_token_router)
