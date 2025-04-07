# Main FastAPI App Entry Point
# backend/main.py

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth, borrower, lender, chatbot
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(borrower.router, prefix="/api/borrower")
app.include_router(lender.router, prefix="/api/lender")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await chatbot.handle_chat(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

