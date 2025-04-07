from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    purpose = Column(String, nullable=False)
    duration_months = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected, paid
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    borrower = relationship("User", backref="loans")
