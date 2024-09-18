
from fastapi import FastAPI

from routers.auth_routers import router as auth_router
from routers.user_routers import router as main_router
from routers.ws_room_router import router as ws_room_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(main_router)
app.include_router(ws_room_router)
