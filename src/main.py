
from fastapi import FastAPI

from src.routers.auth_routers import router as auth_router
from src.routers.auth_user_routes import router as main_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(main_router)
