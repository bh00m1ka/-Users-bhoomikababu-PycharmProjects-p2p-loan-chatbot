from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # "borrower" or "lender"
    language = Column(String, default="en")  # for multilingual support
    bank_account = Column(String, nullable=True)

    # Optional user settings
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
