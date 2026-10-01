from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from app.core.database import get_db
from app.store_recipients.models import StoreRecipient
from app.store_recipients.schemas import *

router = APIRouter(tags=["store_recipients"], prefix="/store_recipients")


@router.get("", response_model=List[StoreRecipientSchema])
async def get_store_recipients(db: Session = Depends(get_db)):
    recipients = db.query(StoreRecipient).all()

    if not recipients:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No store recipients found."},
        )

    return recipients