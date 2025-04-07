from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from models.document import Document
from models.loan import Loan

import uuid
import os

router = APIRouter()

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ProfileUpdate(BaseModel):
    name: str
    language: str
    bank_account: str

@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.role == "lender").first()
    if not user:
        raise HTTPException(status_code=404, detail="Lender not found")
    return user

@router.put("/profile/{user_id}")
def update_profile(user_id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.role == "lender").first()
    if not user:
        raise HTTPException(status_code=404, detail="Lender not found")
    user.name = data.name
    user.language = data.language
    user.bank_account = data.bank_account
    db.commit()
    return {"message": "Profile updated"}

@router.post("/upload-doc")
async def upload_document(
    user_id: int = Form(...),
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
