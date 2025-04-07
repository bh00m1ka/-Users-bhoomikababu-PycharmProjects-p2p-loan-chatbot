
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/borrower")

loans_db = []

@router.post("/loan-request")
def create_loan(data: dict):
    data["id"] = len(loans_db) + 1
    loans_db.append(data)
    return {"message": "Loan request submitted", "loan_id": data["id"]}

@router.get("/loan-requests/{borrower_id}")
def list_loans(borrower_id: int):
    user_loans = [loan for loan in loans_db if loan["borrower_id"] == borrower_id]
    return user_loans

@router.post("/upload-doc/{loan_id}")
async def upload_doc(loan_id: int, file: UploadFile = File(...)):
    content = await file.read()
    # Store or process file (mock here)
    return {"filename": file.filename, "loan_id": loan_id}
