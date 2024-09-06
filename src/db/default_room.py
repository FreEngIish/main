from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class DefaultRoom(Base):
    __tablename__ = 'default_rooms'

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(100), nullable=False)
    native_language = Column(String(10), nullable=False)
    language_level = Column(String(12), nullable=False, default='Beginner')
    participant_limit = Column(Integer, default=10)
    current_participants = Column(Integer, default=0)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String(10), nullable=False, default='Active')

    def __repr__(self):
        return f"<DefaultRoom(room_name={self.room_name}, status={self.status})>"
