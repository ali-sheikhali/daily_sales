from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.stores.models import StoresModel
from app.stores.schemas import *
from app.users.models import UserModels
from typing import List


router = APIRouter(tags=["stores"] ,prefix="/stores")


@router.get("", response_model=List[StoreListSchema])
async def stores_list(db: Session = Depends(get_db)):
    stores = db.query(StoresModel).all()
    return stores

@router.get("/{owner_id}", response_model=List[StoreListSchema])
async def store_detail(
    owner_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    check_owner = db.query(UserModels).filter_by(id=owner_id).first()

    if not check_owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    result = db.query(StoresModel).filter_by(owner_id=owner_id).all()

    return result



@router.post("/")
async def create_stores(request: StoreCreateSchema , db: Session = Depends(get_db)):
    #check if owner exists
    check_owner = db.query(UserModels).filter_by(id = request.owner_id).first()

    if not check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    store = StoresModel(
        name = request.name,
        owner_id = request.owner_id
    )

    # Save to database
    db.add(store)
    db.commit()
    db.refresh(store)

    return store