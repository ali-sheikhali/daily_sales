from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from app.core.database import get_db
from app.store_recipients.models import StoreRecipientModel
from app.store_recipients.schemas import *
from app.stores.models import StoresModel

router = APIRouter(tags=["store_recipients"], prefix="/store_recipients")


# get all store recipients
@router.get("", response_model=List[StoreRecipientSchema])
async def get_store_recipients(db: Session = Depends(get_db)):
    recipients = db.query(StoreRecipientModel).all()

    if not recipients:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No store recipients found."},
        )

    return recipients


# create new store recipient
@router.post("")
async def create_new_store_recipient(request:StoreRecipientCreateSchema, db: Session = Depends(get_db)):

    check_store_id = db.query(StoresModel).filter_by(id = request.store_id).first()

    if not check_store_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store not found"
        )

    new_store_recipient = StoreRecipientModel(
        store_id = request.store_id,
        phone_number = request.phone_number,
    )

    db.add(new_store_recipient)
    db.commit()
    db.refresh(new_store_recipient)

    return new_store_recipient