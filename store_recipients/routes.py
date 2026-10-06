from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from app.core.database import get_db
from app.store_recipients.models import StoreRecipientModel
from app.store_recipients.schemas import *
from app.stores.models import StoresModel
from app.users.dependencies import get_current_user

router = APIRouter(tags=["store_recipients"], prefix="/store_recipients", dependencies=[Depends(get_current_user)])


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
async def create_new_store_recipient(request: StoreRecipientCreateSchema, db: Session = Depends(get_db)):

    check_store_id = db.query(StoresModel).filter_by(
        id=request.store_id).first()

    if not check_store_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store not found"
        )

    new_store_recipient = StoreRecipientModel(
        store_id=request.store_id,
        phone_number=request.phone_number,
    )

    db.add(new_store_recipient)
    db.commit()
    db.refresh(new_store_recipient)

    return new_store_recipient


# get store recipient by store_id
@router.get("/{store_id}", response_model=List[StoreRecipientDetailSchema])
async def get_store_recipient_by_store_id(store_id: int, db: Session = Depends(get_db)):
    store_recipient = db.query(StoreRecipientModel).filter(
        StoreRecipientModel.store_id == store_id).all()

    if not store_recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store recipient not found"
        )

    return store_recipient

# update store recipient by id
@router.patch("/{id}", response_model=StoreRecipientSchema)
async def update_store_recipient(id: int, request: StoreRecipientUpdateSchema, db: Session = Depends(get_db)):
    store_recipient = db.query(StoreRecipientModel).filter(
        StoreRecipientModel.id == id).first()

    if not store_recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store recipient not found"
        )
    
    update_data = request.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(store_recipient, key, value)

    db.commit()  
    db.refresh(store_recipient)
    return store_recipient  

# delete store recipient by id
@router.delete("/{id}")
async def delete_store_recipient(id: int, db: Session = Depends(get_db)):
    store_recipient = db.query(StoreRecipientModel).filter(
        StoreRecipientModel.id == id).first()

    if not store_recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store recipient not found"
        )

    db.delete(store_recipient)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "store recipient deleted successfully."},
    )
