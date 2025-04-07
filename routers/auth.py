from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from sqlalchemy.exc import IntegrityError

router = APIRouter()

class SignUpRequest(BaseModel):
    name: str
    phone_number: str
    role: str  # "borrower" or "lender"
    language: str = "en"

@router.post("/signup")
def signup(data: SignUpRequest, db: Session = Depends(get_db)):
    if data.role not in ["borrower", "lender"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        name=data.name,
        phone_number=data.phone_number,
        role=data.role,
        language=data.language
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered successfully", "user_id": user.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Phone number already registered")
