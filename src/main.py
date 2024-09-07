
from fastapi import FastAPI

from src import auth
from src.routers.main_routes import router as main_router


app = FastAPI()
app.include_router(auth.router)
app.include_router(main_router)
