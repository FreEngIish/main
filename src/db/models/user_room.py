from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class UserRoom(Base):
    __tablename__ = 'user_rooms'

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(100), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    native_language = Column(String(10), nullable=False)
    language_level = Column(String(12), nullable=False, default='Beginner')
    participant_limit = Column(Integer, default=10)
    current_participants = Column(Integer, default=0)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_date = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String(10), nullable=False, default='Active')

    creator = relationship('User', back_populates='user_rooms')
    members = relationship('RoomMembers', back_populates='room')
    messages = relationship('Message', back_populates='room')

    def __repr__(self):
        return f'<UserRoom(room_name={self.room_name}, creator={self.creator_id})>'
