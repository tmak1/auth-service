from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(Integer, primary_key=True) # type: ignore
    username: str = Column(String(50), unique=True, nullable=False) # type: ignore
    password_hash: str = Column(String(200), nullable=False) # type: ignore
    role: str = Column(String(20), default='user') # type: ignore