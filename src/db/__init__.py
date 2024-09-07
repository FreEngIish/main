from .database import Base, engine, database
from .models.user import User
from .models.user_room import UserRoom
from .models.room_members import RoomMembers
from .models.message import Message

# Создаем таблицы
Base.metadata.create_all(bind=engine)
