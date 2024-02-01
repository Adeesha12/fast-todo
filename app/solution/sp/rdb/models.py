from sqlalchemy import TIMESTAMP, Boolean, Column, Date, ForeignKey, Integer, String, DateTime, LargeBinary, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType, EmailType
from solution.sp.rdb.db_connection import Base



class User(Base):
    __tablename__ = 'users'
    UserID = Column(Integer,primary_key=True, index=True)
    Username = Column(String,index=True)
    email = Column(EmailType,index=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512','md5_crypt'],deprecated=['md5_crypt']),index=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    CreatedAt = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP') )
    
    tasks = relationship('Task', back_populates='owner')



class Task(Base):
    __tablename__ = 'todos'
    TaskID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer,ForeignKey("users.UserID", ondelete='CASCADE'),nullable=False)
    TaskTitle = Column(String(255), nullable=False)
    Description = Column(Text)
    DueDate = Column(Date)
    IsComplete = Column(Boolean, default=False)
    CreatedAt = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    owner = relationship('User', back_populates='tasks')

