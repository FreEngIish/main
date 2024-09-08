from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.db.database import Base


class RoomMembers(Base):
    __tablename__ = 'room_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('user_rooms.room_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    room = relationship('UserRoom', back_populates='members')
    user = relationship('User', back_populates='rooms')

    def __repr__(self):
        return f'<RoomMembers(room_id={self.room_id}, user_id={self.user_id})>'
