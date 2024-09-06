from .database import Base, engine, database
from .user import User
from .default_room import DefaultRoom
from .user_room import UserRoom
from .room_members import RoomMembers
from .message import Message

# Создаем таблицы
Base.metadata.create_all(bind=engine)
