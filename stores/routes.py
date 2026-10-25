from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.stores.models import StoresModel
from app.stores.schemas import *
from app.users.models import UserModels
from typing import List
from app.users.dependencies import get_current_user
from app.users.permissions import check_store_access

router = APIRouter(tags=["stores"], prefix="/stores")


@router.get("/all", response_model=List[StoreListSchema])
async def stores_list(db: Session = Depends(get_db)):
    stores = db.query(StoresModel).all()
    return stores


@router.get("", response_model=List[StoreListSchema])
async def store_detail(
    db: Session = Depends(get_db),
    # store: StoresModel = Depends(check_store_access),
    current_user: UserModels = Depends(get_current_user)
):

    if current_user.role == "manager":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to view stores")

    result = db.query(StoresModel).filter_by(owner_id=current_user.id).all()

    return result


@router.post("")
async def create_stores(
    request: StoreCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModels = Depends(get_current_user)
):

    store = StoresModel(
        name=request.name,
        owner_id=current_user.id
    )

    # Save to database
    db.add(store)
    db.commit()
    db.refresh(store)

    return store


@router.delete("/{store_id}")
async def delete_store(store_id: int,
                       db: Session = Depends(get_db),
                       current_user: UserModels = Depends(get_current_user)):

    if current_user.role == "manager":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You are not allowed to delete store")

    store = db.query(StoresModel).filter_by(
        id=store_id, owner_id=current_user.id).first()

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    db.delete(store)
    db.commit()

    return JSONResponse(content={"message": "Store deleted successfully"}, status_code=status.HTTP_200_OK)
