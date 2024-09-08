from .database import Base, engine, database
from src.db.models.user import User
from .models.user_room import UserRoom
from .models.room_members import RoomMembers
from .models.message import Message

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)