from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(30))
    last_name = Column(String(30))
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    auth0_sub = Column(String(255), unique=True)

    user_rooms = relationship('UserRoom', back_populates='creator')
    rooms = relationship('RoomMembers', back_populates='user')
    messages = relationship('Message', back_populates='user')

    def __repr__(self):
        return f'<User(email={self.email}, username={self.username})>'



