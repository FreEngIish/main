from fastapi import FastAPI

from routers.auth_access_token_info import router as auth_acces_token_info
from routers.auth_routes import router as auth_router
from routers.auth_token_routes import router as auth_token_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(auth_token_router)
app.include_router(auth_acces_token_info)
