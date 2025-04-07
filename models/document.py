from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)  # e.g. "ID Proof", "Salary Slip"
    file_url = Column(String, nullable=False)  # stored path or cloud link
    verified = Column(String, default="pending")  # pending, verified, rejected
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="documents")
