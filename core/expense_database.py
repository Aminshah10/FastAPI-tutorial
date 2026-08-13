from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from config import setting

engine = create_engine(
    setting.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False # only for sqlite
}
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    email = Column(String(50))
    
    expenses = relationship("Expense", back_populates="user")
    
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(100))
    amount = Column(Numeric(10, 2), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="expenses")

Base.metadata.create_all(bind=engine)
