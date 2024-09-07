from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('user_rooms.room_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message_text = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship('UserRoom', back_populates='messages')
    user = relationship('User', back_populates='messages')

    def __repr__(self):
        return f'<Message(user_id={self.user_id}, room_id={self.room_id}, message_text={self.message_text})>'
